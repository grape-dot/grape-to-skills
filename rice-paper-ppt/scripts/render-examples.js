// 一式一页：examples/wall-*.html（11 页）→ 同名 *.jpg（1280×720、q92；需 playwright-core + chromium）
const pw = require('D:/nodejs/node_global/node_modules/@playwright/cli/node_modules/playwright-core');
const EXE = 'C:/Users/yanfang/AppData/Local/ms-playwright/chromium-1248/chrome-win64/chrome.exe';
const BASE = 'file:///D:/grape-to-skills/rice-paper-ppt/examples/';
const pages = ['wall-stagger', 'wall-wave', 'wall-depth', 'wall-fan', 'wall-coil', 'wall-sec',
               'wall-crest', 'wall-grid', 'wall-fold', 'wall-arc', 'wall-arc-inner'];
(async () => {
  const browser = await pw.chromium.launch({ executablePath: EXE });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  for (const name of pages) {
    const page = await ctx.newPage();
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto(BASE + name + '.html#1', { waitUntil: 'networkidle' });
    await page.waitForTimeout(600);
    const el = await page.$('.slide.on');
    if (!el) { console.log('NO .slide.on ->', name); await page.close(); continue; }
    await el.screenshot({ path: 'D:/grape-to-skills/rice-paper-ppt/examples/' + name + '.jpg', type: 'jpeg', quality: 92 });
    console.log('ok', name + '.jpg');
    await page.close();
  }
  await browser.close();
})();
