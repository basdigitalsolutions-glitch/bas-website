// Demo tabs (works without JS: first scenario is visible by default)
document.querySelectorAll('.demo').forEach(function (demo) {
  var tabs = demo.querySelectorAll('[role="tab"]');
  tabs.forEach(function (tab, i) {
    tab.addEventListener('click', function () { select(i); });
    tab.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
        var n = (i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length;
        select(n); tabs[n].focus();
      }
    });
  });
  function select(n) {
    tabs.forEach(function (t, j) {
      t.setAttribute('aria-selected', j === n ? 'true' : 'false');
      t.tabIndex = j === n ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = j !== n;
    });
  }
  select(0);
});
// Close the mobile menu after choosing a link
document.querySelectorAll('details.menu a').forEach(function (a) {
  a.addEventListener('click', function () { a.closest('details').removeAttribute('open'); });
});
