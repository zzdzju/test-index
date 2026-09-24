(function () {
  /* 右侧顾客咨询：展开 / 收起 */
  var box = document.getElementById('consult');
  var tab = document.getElementById('consultTab');
  var closeBtn = document.getElementById('consultClose');
  function openBox() { box && box.classList.add('open'); }
  function closeBox() { box && box.classList.remove('open'); }
  if (tab) {
    tab.addEventListener('click', function (e) {
      e.stopPropagation();
      box.classList.contains('open') ? closeBox() : openBox();
    });
  }
  if (closeBtn) closeBtn.addEventListener('click', closeBox);
  document.addEventListener('click', function (e) {
    if (box && box.classList.contains('open') && !box.contains(e.target)) closeBox();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeBox();
  });

  /* 任意"咨询"触发按钮 */
  Array.prototype.forEach.call(document.querySelectorAll('[data-open-consult]'), function (el) {
    el.addEventListener('click', function (e) { e.preventDefault(); openBox(); });
  });

  /* 表单：原型不提交，仅本地反馈 */
  var form = document.getElementById('consultForm');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = document.getElementById('consultOk');
      if (ok) ok.style.display = 'block';
      form.style.display = 'none';
    });
  }

  /* 回到顶部 */
  var toTop = document.getElementById('toTop');
  function syncTop() {
    if (!toTop) return;
    toTop.style.display = window.scrollY > 300 ? '' : 'none';
  }
  if (toTop) {
    toTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
    window.addEventListener('scroll', syncTop);
    syncTop();
  }
})();

(function () {
  /* 首页顶部轮播：横向滑动 + 自动播放 + 箭头 / 圆点 / 触摸 / 键盘 */
  var root = document.getElementById('heroSlider');
  if (!root) return;
  var track = root.querySelector('.slider-track');
  var slides = root.querySelectorAll('.slide');
  var dots = root.querySelectorAll('.dot');
  var prev = root.querySelector('.is-prev');
  var next = root.querySelector('.is-next');
  var total = slides.length;
  if (!track || total < 2) return;

  var idx = 0;
  var timer = null;
  var gap = parseInt(root.getAttribute('data-interval'), 10) || 5200;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function resetBar() {
    var fill = root.querySelector('.dot.is-active .dot-fill');
    if (!fill) return;
    fill.style.animation = 'none';
    void fill.offsetWidth;
    fill.style.animation = '';
  }
  function render() {
    track.style.transform = 'translateX(' + (-idx * 100) + '%)';
    resetBar();
    for (var i = 0; i < total; i++) {
      var on = i === idx;
      slides[i].classList.toggle('is-active', on);
      slides[i].setAttribute('aria-hidden', on ? 'false' : 'true');
      if (dots[i]) {
        dots[i].classList.toggle('is-active', on);
        dots[i].setAttribute('aria-selected', on ? 'true' : 'false');
      }
    }
  }
  function go(n) { idx = ((n % total) + total) % total; render(); }
  function stop() {
    if (timer) { clearInterval(timer); timer = null; }
    root.classList.add('is-hold');
  }
  function start() {
    if (reduce) return;
    stop();
    root.style.setProperty('--slide-dur', gap + 'ms');
    root.classList.remove('is-hold');
    resetBar();
    timer = setInterval(function () { go(idx + 1); }, gap);
  }
  function jump(n) { stop(); go(n); start(); }

  if (prev) prev.addEventListener('click', function () { jump(idx - 1); });
  if (next) next.addEventListener('click', function () { jump(idx + 1); });

  Array.prototype.forEach.call(dots, function (d) {
    d.addEventListener('click', function () {
      jump(parseInt(d.getAttribute('data-index'), 10) || 0);
    });
  });

  /* 鼠标悬停 / 获得焦点时暂停，离开后继续 */
  root.addEventListener('mouseenter', stop);
  root.addEventListener('mouseleave', start);
  root.addEventListener('focusin', stop);
  root.addEventListener('focusout', start);

  /* 键盘左右方向键 */
  root.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { jump(idx - 1); }
    else if (e.key === 'ArrowRight') { jump(idx + 1); }
  });

  /* 触摸滑动（手机） */
  var startX = 0, startY = 0, swiping = false;
  root.addEventListener('touchstart', function (e) {
    startX = e.touches[0].clientX;
    startY = e.touches[0].clientY;
    swiping = true;
    stop();
  }, { passive: true });
  root.addEventListener('touchend', function (e) {
    if (!swiping) return;
    swiping = false;
    var dx = e.changedTouches[0].clientX - startX;
    var dy = e.changedTouches[0].clientY - startY;
    if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) go(dx < 0 ? idx + 1 : idx - 1);
    start();
  }, { passive: true });

  /* 页面切到后台时暂停，回来再继续 */
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) { stop(); } else { start(); }
  });

  render();
  start();
})();
