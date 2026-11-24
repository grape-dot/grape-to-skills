// 幻灯片控制：自适应缩放、翻页、目录定位、打印
(function () {
  const deck = document.getElementById('deck');
  const slides = Array.from(deck.querySelectorAll('.slide'));
  const hud = document.querySelector('.hud');
  const pbar = document.querySelector('.pbar');
  let cur = 0;

  function fit() {
    const s = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
    deck.style.transform = `scale(${s})`;
    deck.style.left = (window.innerWidth - 1280 * s) / 2 + 'px';
    deck.style.top = (window.innerHeight - 720 * s) / 2 + 'px';
  }

  function show(i, push) {
    cur = Math.max(0, Math.min(slides.length - 1, i));
    slides.forEach((s, k) => {
      const on = k === cur;
      s.classList.toggle('on', on);
      s.querySelectorAll('video').forEach((v) => {
        if (on) {
          const p = v.play();
          if (p && p.catch) p.catch(() => {});
        } else {
          v.pause();
        }
      });
    });
    if (hud) hud.textContent = String(cur + 1).padStart(2, '0') + ' / ' + slides.length;
    if (pbar) pbar.style.width = ((cur + 1) / slides.length) * 100 + '%';
    if (push !== false) history.replaceState(null, '', '#' + (cur + 1));
  }

  // 静音自动播是浏览器强制的，声音只能靠一次点击放开
  document.addEventListener('click', (e) => {
    const b = e.target.closest && e.target.closest('.snd');
    if (!b) return;
    const v = document.getElementById(b.dataset.for) || b.parentElement.querySelector('video');
    if (!v) return;
    v.muted = false;
    v.volume = 1;
    const p = v.play();
    if (p && p.catch) p.catch(() => {});
    b.classList.add('gone');
    b.blur();
  });

  document.addEventListener('keydown', (e) => {
    // 焦点在视频上时，空格和方向键交给播放器
    if (e.target && e.target.tagName === 'VIDEO') return;
    const k = e.key;
    if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown' || k === ' ') {
      e.preventDefault(); show(cur + 1);
    } else if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp') {
      e.preventDefault(); show(cur - 1);
    } else if (k === 'Home') {
      show(0);
    } else if (k === 'End') {
      show(slides.length - 1);
    } else if (k === 'f' || k === 'F') {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    } else if (k === 'p' || k === 'P') {
      window.print();
    } else if (/^[0-9]$/.test(k)) {
      pending += k;
      clearTimeout(pendingTimer);
      pendingTimer = setTimeout(() => { show(parseInt(pending, 10) - 1); pending = ''; }, 450);
    }
  });

  let pending = '';
  let pendingTimer = null;

  if (window.location.search.indexOf('shot') > -1) document.body.classList.add('shot');

  const start = parseInt((location.hash || '#1').slice(1), 10);
  show(isNaN(start) ? 0 : start - 1, false);
  fit();
  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', () => {
    const n = parseInt((location.hash || '#1').slice(1), 10);
    if (!isNaN(n)) show(n - 1, false);
  });
})();
