/* Лендинг «Опора» — вся интерактивность страницы.
   Формы ничего никуда не отправляют: это демонстрационный макет. */
(function () {
  'use strict';

  // ── тень у шапки при прокрутке ────────────────────────────────────
  var header = document.querySelector('.header');
  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 8); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // ── мобильное меню ────────────────────────────────────────────────
  var burger = document.getElementById('burger');
  var nav = document.getElementById('nav');
  burger.addEventListener('click', function () {
    burger.classList.toggle('open');
    nav.classList.toggle('open');
  });
  nav.addEventListener('click', function (e) {
    if (e.target.tagName === 'A') {
      burger.classList.remove('open');
      nav.classList.remove('open');
    }
  });

  // ── аккордеон вопросов ────────────────────────────────────────────
  // max-height считаем по фактической высоте ответа, иначе длинные
  // тексты обрезаются, а короткие открываются с задержкой.
  document.querySelectorAll('.q__btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var q = btn.parentElement;
      var a = q.querySelector('.q__a');
      var open = q.classList.contains('open');
      document.querySelectorAll('.q.open').forEach(function (other) {
        other.classList.remove('open');
        other.querySelector('.q__a').style.maxHeight = null;
      });
      if (!open) {
        q.classList.add('open');
        a.style.maxHeight = a.scrollHeight + 'px';
      }
    });
  });

  // ── формы-заглушки ────────────────────────────────────────────────
  document.querySelectorAll('.js-form').forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = form.querySelector('.form__ok');
      var note = form.querySelector('.form__note');
      form.querySelectorAll('.inp').forEach(function (i) { i.value = ''; });
      if (ok) ok.classList.add('on');
      if (note) note.style.display = 'none';
      setTimeout(function () {
        if (ok) ok.classList.remove('on');
        if (note) note.style.display = '';
      }, 4500);
    });
  });

  // ── появление блоков при прокрутке ────────────────────────────────
  var targets = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('on'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('on');
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -12% 0px' });
  targets.forEach(function (el) { io.observe(el); });
})();
