/* 增强层（可选）：图墙入场与实际特效的编排。
 *
 * HTML 是交付载体，不是能力上限。静态版式由 theme.css 负责，并且必须在不执行 JS 时就正确；
 * 这一层只负责「动」——可以接 GSAP，也可以接 WebGL / Canvas2D，通过 RP.fx.register 挂载。
 *
 * 三条底线（约束的是交付物，不是技术选型）：
 *   1. 静态回退：没有 JS、断网、依赖缺失时，版面已经是对的；本文件不改任何布局尺寸。
 *   2. 依赖本地化：gsap 放 assets/vendor/；CDN 只能作为可选回退，不能是唯一来源。
 *   3. 三种场景回到终态：打印、截图模式（?shot）、prefers-reduced-motion。
 *
 * 引入顺序：gsap（可选）→ fx.js → deck.js
 */
(function () {
  'use strict';

  var RP = (window.RP = window.RP || {});
  var fx = (RP.fx = RP.fx || {});
  var recipes = {};
  var mounted = [];

  var reduce = !!(window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  var gsap = window.gsap;

  /* 注册自定义配方：RP.fx.register(name, function (el, api) { ... return cleanup })
   * el 是带 data-fx="name" 的元素；api = { gsap, reduce, toArray }。
   * 返回的函数会在离开该页时调用——WebGL 上下文、纹理、rAF 都在这里回收。 */
  fx.register = function (name, fn) {
    if (typeof fn === 'function') recipes[name] = fn;
    return fx;
  };

  fx.available = !!gsap && !reduce;

  // 没有 GSAP 或用户要求减弱动效：完全不接管，theme.css 的 CSS 入场继续生效
  if (!fx.available) return;

  var EASE = 'power2.out';
  var BUILT_IN = '.w-stag .pc, .w-wave, .w-fan, .w-fan img, .w-depth';

  function play(slide) {
    if (!slide) return;
    if (document.body && document.body.classList.contains('shot')) return;

    var stag = slide.querySelector('.w-stag');
    if (stag && stag.querySelector('.pc')) {
      gsap.fromTo(stag.querySelectorAll('.pc'),
        { y: 24, opacity: 0 },
        { y: 0, opacity: 1, duration: .7, stagger: .08, ease: EASE, clearProps: 'transform,opacity' });
    }

    var wave = slide.querySelector('.w-wave');
    if (wave) {
      gsap.fromTo(wave, { y: 24, opacity: 0 },
        { y: 0, opacity: 1, duration: .8, ease: EASE, clearProps: 'transform,opacity' });
    }

    var fan = slide.querySelector('.w-fan');
    if (fan) {
      gsap.fromTo(fan, { y: 20, opacity: 0 },
        { y: 0, opacity: 1, duration: .7, ease: EASE, clearProps: 'transform,opacity' });
      gsap.fromTo(fan.querySelectorAll('img'), { opacity: 0, y: 16 },
        { opacity: 1, y: 0, duration: .55, stagger: .07, delay: .1, ease: EASE, clearProps: 'transform,opacity' });
    }

    // 纵深墙必须带 transformPerspective，否则 rotateY 会丢掉透视
    var depth = slide.querySelector('.w-depth');
    if (depth) {
      gsap.fromTo(depth,
        { rotateY: -38, transformPerspective: 1600, opacity: 0 },
        { rotateY: -25, transformPerspective: 1600, opacity: 1, duration: .9, ease: EASE, clearProps: 'transform,opacity' });
    }

    mountCustom(slide);
  }

  function mountCustom(slide) {
    Array.prototype.forEach.call(slide.querySelectorAll('[data-fx]'), function (el) {
      var names = (el.getAttribute('data-fx') || '').split(/\s+/);
      names.forEach(function (name) {
        if (!name) return;
        var fn = recipes[name];
        if (!fn) {
          console.warn('[RP.fx] 未注册的配方：' + name);
          return;
        }
        var cleanup = null;
        try {
          cleanup = fn(el, { gsap: gsap, reduce: reduce, toArray: gsap.utils.toArray });
        } catch (err) {
          console.warn('[RP.fx] 配方执行失败：' + name, err);
          return;
        }
        mounted.push({ el: el, cleanup: typeof cleanup === 'function' ? cleanup : null });
      });
    });
  }

  function unmount() {
    mounted.forEach(function (m) {
      if (!m.cleanup) return;
      try { m.cleanup(); } catch (err) { console.warn('[RP.fx] 清理失败', err); }
    });
    mounted = [];
  }

  var deck = document.getElementById('deck');
  if (!deck) return;

  // 提前关掉 theme.css 的 CSS 入场，避免与 GSAP 双重动画（脚本须在 deck.js 之前引入）
  document.documentElement.classList.add('fx-js');

  var current = null;

  function activate(slide) {
    if (!slide || slide === current) return;
    unmount();
    current = slide;
    play(slide);
  }

  // 不依赖 deck.js 的内部实现：监听 .slide 的 class 变化即可
  new MutationObserver(function (records) {
    for (var i = 0; i < records.length; i++) {
      var t = records[i].target;
      if (t.classList && t.classList.contains('slide') && t.classList.contains('on')) activate(t);
    }
  }).observe(deck, { attributes: true, attributeFilter: ['class'], subtree: true });

  window.addEventListener('load', function () {
    activate(deck.querySelector('.slide.on'));
  });

  // 打印前冻结到静态终态，避免 tween 中途被截进 PDF
  window.addEventListener('beforeprint', function () {
    unmount();
    gsap.killTweensOf(BUILT_IN);
    gsap.set(BUILT_IN, { clearProps: 'all' });
  });
})();
