(() => {
  'use strict';
  const sidebar = document.getElementById('sidebar');
  const toggle = document.getElementById('menuBtn');
  const closeBtn = document.getElementById('menuClose');
  const scrim = document.getElementById('scrim');
  if (!sidebar || !toggle || !scrim) return;
  let previousFocus = null;
  const mobile = window.matchMedia('(max-width: 900px)');
  function setMenu(open, restoreFocus = true) {
    const shouldOpen = Boolean(open && mobile.matches);
    const wasOpen = sidebar.classList.contains('open');
    sidebar.classList.toggle('open', shouldOpen);
    scrim.classList.toggle('show', shouldOpen);
    document.body.classList.toggle('body-menu-open', shouldOpen);
    toggle.setAttribute('aria-expanded', String(shouldOpen));
    toggle.setAttribute('aria-label', shouldOpen ? 'Close navigation menu' : 'Open navigation menu');
    sidebar.setAttribute('aria-hidden', String(mobile.matches && !shouldOpen));
    if (shouldOpen && !wasOpen) {
      previousFocus = document.activeElement;
      closeBtn?.focus();
    } else if (!shouldOpen && wasOpen && restoreFocus) {
      (previousFocus && previousFocus.isConnected ? previousFocus : toggle).focus();
    }
  }
  toggle.addEventListener('click', () => setMenu(!sidebar.classList.contains('open')));
  closeBtn?.addEventListener('click', () => setMenu(false));
  scrim.addEventListener('click', () => setMenu(false));
  sidebar.querySelectorAll('a').forEach(link => link.addEventListener('click', () => setMenu(false, false)));
  document.addEventListener('keydown', evt => {
    if (!sidebar.classList.contains('open')) return;
    if (evt.key === 'Escape') { evt.preventDefault(); setMenu(false); return; }
    if (evt.key === 'Tab') {
      const targets = [...sidebar.querySelectorAll('a[href], button:not([disabled])')].filter(el => el.getClientRects().length);
      if (!targets.length) return;
      const first = targets[0], last = targets[targets.length-1];
      if (evt.shiftKey && document.activeElement === first) {evt.preventDefault();last.focus();}
      else if (!evt.shiftKey && document.activeElement === last) {evt.preventDefault();first.focus();}
    }
  });
  const sync = () => setMenu(false, false);
  if (mobile.addEventListener) mobile.addEventListener('change',sync);
  else mobile.addListener(sync);
  sync();
})();