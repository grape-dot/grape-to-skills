#!/usr/bin/env node
/**
 * HTML 幻灯片版式审计：逐页真实渲染 → 抓溢出/裁切/小字号 → 顺带出图
 *
 * 用法：
 *   node audit.js <url> [outDir] [--no-shots]
 *   node audit.js http://localhost:8000/deck.html ./shots
 *
 * 依赖（任选一种）：
 *   npm i -D playwright-core && npx playwright install chromium
 *   npm i playwright                     # 自带浏览器下载
 *   或已有 Chrome：设 CHROME_PATH 指过去即可
 *
 * 环境变量（都可选）：
 *   CHROME_PATH  Chromium/Chrome 可执行文件路径
 *   PW_CORE      playwright-core 模块路径（装在非常规位置时用）
 *
 * 退出码：发现问题 → 1；全部通过 → 0。便于串进脚本里当闸门。
 */
const path = require('path');
const fs = require('fs');
const os = require('os');

function loadPlaywright() {
  const tries = [
    process.env.PW_CORE,
    'playwright-core',
    'playwright',
    path.join(process.cwd(), 'node_modules/playwright-core'),
    '/usr/lib/node_modules/playwright-core',
    '/usr/local/lib/node_modules/playwright-core',
  ].filter(Boolean);
  const errs = [];
  for (const t of tries) {
    try { return require(t); } catch (e) { errs.push(t + ': ' + e.code); }
  }
  console.error(
    '找不到 playwright-core。安装方式：\n' +
    '  npm i -D playwright-core && npx playwright install chromium\n' +
    '已尝试：\n  ' + errs.join('\n  ')
  );
  process.exit(2);
}

/** 在没有随包装浏览器时，找本机可用的 Chromium / Chrome */
function findChrome() {
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;

  const home = os.homedir();
  const pwRoots = [
    path.join(home, 'AppData/Local/ms-playwright'),
    path.join(home, 'Library/Caches/ms-playwright'),
    path.join(home, '.cache/ms-playwright'),
  ];
  const inner = [
    'chrome-win64/chrome.exe',
    'chrome-win/chrome.exe',
    'chrome-linux/chrome',
    'chrome-mac/Chromium.app/Contents/MacOS/Chromium',
    'chrome-mac-x64/Chromium.app/Contents/MacOS/Chromium',
    'chrome-mac-arm64/Chromium.app/Contents/MacOS/Chromium',
  ];
  for (const root of pwRoots) {
    if (!fs.existsSync(root)) continue;
    const builds = fs.readdirSync(root).filter((d) => /^chromium-\d+$/.test(d)).sort().reverse();
    for (const b of builds) {
      for (const i of inner) {
        const p = path.join(root, b, i);
        if (fs.existsSync(p)) return p;
      }
    }
  }

  const system = [
    'C:/Program Files/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
  ];
  for (const p of system) if (fs.existsSync(p)) return p;
  return null;
}

const { chromium } = loadPlaywright();

const url = process.argv[2];
if (!url) {
  console.error('用法: node audit.js <url> [outDir] [--no-shots]');
  process.exit(2);
}
const outDir = path.resolve(process.argv[3] && !process.argv[3].startsWith('--') ? process.argv[3] : 'shots');
const wantShots = !process.argv.includes('--no-shots');

(async () => {
  const chrome = findChrome();
  const launchOpts = chrome ? { executablePath: chrome } : {};
  let browser;
  try {
    browser = await chromium.launch(launchOpts);
  } catch (e) {
    console.error(
      '浏览器启动失败：' + e.message + '\n' +
      (chrome ? '已尝试：' + chrome + '\n' : '') +
      '请先 npx playwright install chromium，或用 CHROME_PATH 指定 chrome 可执行文件'
    );
    process.exit(2);
  }

  const page = await browser.newPage({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  const errors = [];
  const IGNORE = /favicon/i;
  page.on('console', (m) => {
    if (m.type() !== 'error') return;
    const u = (m.location && m.location().url) || '';
    if (IGNORE.test(m.text()) || IGNORE.test(u)) return;
    errors.push(m.text() + (u ? ' @' + u.split('/').pop() : ''));
  });
  page.on('pageerror', (e) => errors.push('PAGEERROR ' + e.message));
  const http4xx = [];
  page.on('response', (r) => { if (r.status() >= 400 && !IGNORE.test(r.url())) http4xx.push(r.status() + ' ' + r.url().split('/').pop()); });

  await page.goto(url, { waitUntil: 'load' });
  await page.waitForTimeout(1500);

  const report = await page.evaluate(() => {
    const slides = [...document.querySelectorAll('.slide')];
    const res = [];
    slides.forEach((s, i) => {
      const sr = s.getBoundingClientRect();

      // ① 元素越出画布
      const out = [];
      s.querySelectorAll('*').forEach((el) => {
        const r = el.getBoundingClientRect();
        if (r.width < 1 || r.height < 1) return;
        const db = r.bottom - sr.bottom, dr = r.right - sr.right, dt = sr.top - r.top, dl = sr.left - r.left;
        if (db > 1 || dr > 1 || dt > 1 || dl > 1) {
          const cls = typeof el.className === 'string' ? el.className : '';
          out.push(`${el.tagName}.${cls}`.slice(0, 40) + ` [b${Math.round(db)} r${Math.round(dr)} t${Math.round(dt)} l${Math.round(dl)}]`);
        }
      });

      // ② 内部被裁切（scrollHeight 大于可视高度）
      const clip = [];
      s.querySelectorAll('div,p,table,td,th,h1,h2,li,span').forEach((el) => {
        const st = getComputedStyle(el);
        const named = /pbox|card|code|term|col|bar|frame/.test(el.className);
        const dz = el.scrollHeight - el.clientHeight, dw = el.scrollWidth - el.clientWidth;
        if ((st.overflow === 'hidden' || named) && (dz > 2 || dw > 2)) {
          clip.push(`${el.tagName}.${el.className}`.slice(0, 40));
        }
      });

      // ③ 小于 15px 的文本（页码/图注等 12–14px 微标签会照常列出，人工判断）
      const tiny = new Set();
      s.querySelectorAll('div,span,p,td,th,li,a').forEach((el) => {
        if (!el.textContent.trim() || el.children.length) return;
        const fs = parseFloat(getComputedStyle(el).fontSize);
        if (fs < 15) tiny.add(Math.round(fs) + 'px:' + el.textContent.trim().slice(0, 12));
      });

      // ④ 容器内容溢出内边距
      const spill = [];
      s.querySelectorAll('.pbox,.card,.col,.bar').forEach((box) => {
        const br = box.getBoundingClientRect();
        const pb = parseFloat(getComputedStyle(box).paddingBottom) || 0;
        let maxb = 0;
        box.querySelectorAll(':scope > *').forEach((el) => { const r = el.getBoundingClientRect(); if (r.height > 0) maxb = Math.max(maxb, r.bottom); });
        if (maxb - (br.bottom - pb) > 2) spill.push((box.className || box.tagName).slice(0, 22) + ' +' + Math.round(maxb - (br.bottom - pb)));
      });

      // ⑤ 内容区 .sb 底部溢出（最常见的“静默裁切”）
      let sbOver = 0;
      s.querySelectorAll('.sb').forEach((sb) => {
        const br = sb.getBoundingClientRect();
        sb.querySelectorAll('*').forEach((el) => {
          const r = el.getBoundingClientRect();
          if (r.height > 0) sbOver = Math.max(sbOver, r.bottom - br.bottom);
        });
      });

      if (out.length || clip.length || tiny.size || sbOver > 2 || spill.length) {
        res.push({ p: i + 1, sb: Math.round(sbOver), spill: spill.slice(0, 4), out: out.slice(0, 6), clip: clip.slice(0, 4), tiny: [...tiny].slice(0, 4) });
      }
    });
    return { total: slides.length, res };
  });

  // 人读摘要
  const hard = report.res.filter((r) => r.sb > 0 || r.out.length || r.clip.length || r.spill.length);
  console.log(`页数 ${report.total}｜硬问题页 ${hard.length}｜含微标签页 ${report.res.length}`);
  for (const r of hard) {
    console.log(`  P${r.p}  sb+${r.sb}  out:${r.out.join(' ')}  clip:${r.clip.join(' ')}  spill:${r.spill.join(' ')}`);
  }
  const tinyPages = report.res.filter((r) => r.tiny.length && !hard.includes(r));
  if (tinyPages.length) console.log('  仅小字号（人工判断是否为页码/图注）: ' + tinyPages.map((r) => 'P' + r.p).join(','));
  if (http4xx.length) console.log('  4xx: ' + [...new Set(http4xx)].slice(0, 6).join(', '));
  if (errors.length) console.log('  控制台报错: ' + errors.slice(0, 4).join(' | '));
  console.log(JSON.stringify(report, null, 1));

  if (wantShots) {
    fs.mkdirSync(outDir, { recursive: true });
    for (let i = 0; i < report.total; i++) {
      await page.evaluate((k) => { location.hash = String(k + 1); }, i);
      await page.waitForTimeout(90);
      await page.screenshot({ path: path.join(outDir, `p${String(i + 1).padStart(2, '0')}.png`) });
    }
    console.log('截图 → ' + outDir);
  }

  await browser.close();
  process.exit(hard.length ? 1 : 0);
})();
