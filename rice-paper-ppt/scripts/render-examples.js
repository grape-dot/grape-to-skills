// 渲染 scripts 里 11 式示例页 → examples/*.jpg（1280×720、q92；需 playwright-core + chromium）
const pw = require('D:/nodejs/node_global/node_modules/@playwright/cli/node_modules/playwright-core');
const EXE = 'C:/Users/yanfang/AppData/Local/ms-playwright/chromium-1248/chrome-win64/chrome.exe';
const BASE = 'file:///D:/grape-to-skills/rice-paper-ppt/examples/';
const jobs = [
  ['wall-four.html', 1, 'wall-stagger.jpg'],
  ['wall-four.html', 2, 'wall-wave.jpg'],
  ['wall-four.html', 3, 'wall-depth.jpg'],
  ['wall-four.html', 4, 'wall-fan.jpg'],
  ['wall-coil.html', 1, 'wall-coil.jpg'],
  ['wall-sec-crest.html', 1, 'wall-sec.jpg'],
  ['wall-sec-crest.html', 2, 'wall-crest.jpg'],
  ['wall-curve.html', 1, 'wall-grid.jpg'],
  ['wall-curve.html', 2, 'wall-fold.jpg'],
  ['wall-curve.html', 3, 'wall-arc.jpg'],
  ['wall-curve.html', 4, 'wall-arc-inner.jpg'],
];
(async () => {
  const browser = await pw.chromium.launch({ executablePath: EXE });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 1 });
  for (const [file, n, out] of jobs) {
    const page = await ctx.newPage();
    await page.emulateMedia({ reducedMotion: 'reduce' });
    await page.goto(BASE + file + '#' + n, { waitUntil: 'networkidle' });
    await page.waitForTimeout(600);
    const el = await page.$('.slide.on');
    if (!el) { console.log('NO .slide.on ->', file, n); await page.close(); continue; }
    await el.screenshot({ path: 'D:/grape-to-skills/rice-paper-ppt/examples/' + out, type: 'jpeg', quality: 92 });
    console.log('ok', out);
    await page.close();
  }
  await browser.close();
})();
