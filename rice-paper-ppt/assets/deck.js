// 幻灯片控制：自适应缩放、翻页、目录定位、页码、视频控件、打印
(function () {
  const deck = document.getElementById('deck');
  const slides = Array.from(deck.querySelectorAll('.slide'));
  const hud = document.querySelector('.hud');
  const pbar = document.querySelector('.pbar');
  let cur = 0;

  // 页码：统一写成「当前页 / 总页」，按 DOM 顺序自动填，手写数字只作兜底
  const pad = (n) => String(n).padStart(2, '0');
  slides.forEach((s, i) => {
    const pn = s.querySelector('.pn, .sec-pn, .cv-pn, .end-pn');
    if (pn) pn.textContent = pad(i + 1) + ' / ' + slides.length;
  });

  // 视频控件：给每个 .vid 容器补「播放 / 暂停 + 可拖拽进度条」
  const ICON_PLAY = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.1v13.8L19.2 12z"/></svg>';
  const ICON_PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="7" y="5" width="3.6" height="14" rx="1.1"/><rect x="13.4" y="5" width="3.6" height="14" rx="1.1"/></svg>';
  const mmss = (t) => {
    if (!isFinite(t) || t < 0) t = 0;
    const m = Math.floor(t / 60), s = Math.floor(t % 60);
    return m + ':' + String(s).padStart(2, '0');
  };

  document.querySelectorAll('.vid').forEach((box) => {
    const v = box.querySelector('video');
    if (!v || box.querySelector('.vctl')) return;

    const ctl = document.createElement('div');
    ctl.className = 'vctl';
    ctl.innerHTML =
      '<button class="vpp" type="button" aria-label="播放 / 暂停">' + ICON_PLAY + '</button>' +
      '<div class="vbar" role="slider" tabindex="0" aria-label="播放进度" title="点击或拖动跳转">' +
        '<div class="vtrack"><div class="vfill"></div></div>' +
      '</div>' +
      '<span class="vtime">0:00 / 0:00</span>';
    box.appendChild(ctl);

    const pp = ctl.querySelector('.vpp');
    const bar = ctl.querySelector('.vbar');
    const fill = ctl.querySelector('.vfill');
    const time = ctl.querySelector('.vtime');

    function paint() {
      const d = isFinite(v.duration) ? v.duration : 0;
      const c = isFinite(v.currentTime) ? v.currentTime : 0;
      fill.style.width = (d ? Math.min(100, (c / d) * 100) : 0) + '%';
      time.textContent = mmss(c) + ' / ' + mmss(d);
      pp.innerHTML = v.paused ? ICON_PLAY : ICON_PAUSE;
    }

    function toggle() {
      if (v.paused) {
        const p = v.play();
        if (p && p.catch) p.catch(() => {});
      } else {
        v.pause();
      }
    }

    let dragging = false;
    function seekTo(e) {
      const r = bar.getBoundingClientRect();
      if (!r.width) return;
      const ratio = Math.min(1, Math.max(0, (e.clientX - r.left) / r.width));
      if (isFinite(v.duration) && v.duration > 0) v.currentTime = ratio * v.duration;
      paint();
    }

    pp.addEventListener('click', (e) => { e.stopPropagation(); toggle(); });
    v.addEventListener('click', toggle);
    bar.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      dragging = true;
      if (bar.setPointerCapture) bar.setPointerCapture(e.pointerId);
      seekTo(e);
    });
    bar.addEventListener('pointermove', (e) => { if (dragging) seekTo(e); });
    bar.addEventListener('pointerup', () => { dragging = false; });
    bar.addEventListener('pointercancel', () => { dragging = false; });
    bar.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      e.preventDefault();
      e.stopPropagation();
      const step = e.key === 'ArrowRight' ? 1 : -1;
      v.currentTime = Math.min(v.duration || 0, Math.max(0, v.currentTime + step));
      paint();
    });
    ['loadedmetadata', 'durationchange', 'timeupdate', 'play', 'pause', 'seeked'].forEach((ev) =>
      v.addEventListener(ev, paint)
    );
    paint();
  });

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
