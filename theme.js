/* Shared helpers for all pages of Mikan's Corner:
   - theme switcher (dark default / light, remembered in localStorage)
   - a tiny animation-pause helper so the cat stops drawing in hidden tabs */
(function () {
  var KEY = 'mikan-theme';
  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  var theme = saved || (window.matchMedia &&
    window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
  document.documentElement.dataset.theme = theme;

  window.mikanTheme = {
    current: function () { return document.documentElement.dataset.theme; },
    toggle: function () {
      var next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
      document.documentElement.dataset.theme = next;
      try { localStorage.setItem(KEY, next); } catch (e) {}
      return next;
    }
  };

  /* Runs `tick` on an interval, but pauses while the tab is hidden so we
     don't burn a timer (or battery) drawing a canvas nobody can see. */
  window.mikanEvery = function (ms, tick) {
    var timer = setInterval(tick, ms);
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) {
        clearInterval(timer); timer = null;
      } else if (!timer) {
        timer = setInterval(tick, ms);
      }
    });
    return function stop() { if (timer) { clearInterval(timer); timer = null; } };
  };

  /* follow the system theme live, until the visitor picks one themselves */
  if (window.matchMedia) {
    var mq = window.matchMedia('(prefers-color-scheme: light)');
    var onSys = function (e) {
      var picked = null;
      try { picked = localStorage.getItem(KEY); } catch (err) {}
      if (!picked) document.documentElement.dataset.theme = e.matches ? 'light' : 'dark';
    };
    if (mq.addEventListener) mq.addEventListener('change', onSys);
    else if (mq.addListener) mq.addListener(onSys);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var btns = document.querySelectorAll('.theme-toggle');
    for (var i = 0; i < btns.length; i++) {
      (function (btn) {
        function paint() {
          var isLight = window.mikanTheme.current() === 'light';
          btn.textContent = isLight ? '🌙' : '☀️';
          btn.setAttribute('aria-label', isLight ? 'Switch to dark theme' : 'Switch to light theme');
          btn.title = btn.getAttribute('aria-label');
        }
        paint();
        btn.addEventListener('click', function () { window.mikanTheme.toggle(); paint(); });
      })(btns[i]);
    }
  });
})();
