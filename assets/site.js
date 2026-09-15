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
