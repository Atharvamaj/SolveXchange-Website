// menu stuff lives here
function showSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;
    sidebar.style.display = 'flex';
    document.body.classList.add('menu-open');
    document.querySelector('.menubutton a')?.setAttribute('aria-expanded', 'true');
    sidebar.querySelector('a')?.focus();
}
function hideSidebar(restoreFocus = true) {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar || sidebar.style.display !== 'flex') return;
    sidebar.style.display = 'none';
    document.body.classList.remove('menu-open');
    const open = document.querySelector('.menubutton a');
    open?.setAttribute('aria-expanded', 'false');
    if (restoreFocus) open?.focus();
}
document.addEventListener('keydown', event => {
    if (event.key === 'Escape') hideSidebar();
});

// let the keyboard open the menu and extra bits too
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const open = document.querySelector('.menubutton a');
    const close = document.querySelector('.xbutton a');
    if (sidebar) {
        sidebar.id = 'mobile-navigation';
        sidebar.setAttribute('aria-label', 'Mobile navigation');
    }
    for (const [control, label] of [[open, 'Open navigation'], [close, 'Close navigation']]) {
        if (!control) continue;
        control.setAttribute('role', 'button');
        control.setAttribute('aria-label', label);
        control.setAttribute('aria-controls', 'mobile-navigation');
        control.addEventListener('keydown', event => {
            if (event.key === ' ') { event.preventDefault(); control.click(); }
        });
    }
    if (open) open.setAttribute('aria-expanded', 'false');
    document.querySelectorAll('label[onclick^="expandDiv"]').forEach(control => {
        const match = control.getAttribute('onclick').match(/expandDiv\('([^']+)'\)/);
        const content = match && document.getElementById(match[1]);
        if (!content) return;
        control.setAttribute('role', 'button');
        control.tabIndex = 0;
        control.setAttribute('aria-controls', content.id);
        control.setAttribute('aria-expanded', 'false');
        const question = control.parentElement.textContent.replace(/^[+−-]\s*/, '').trim();
        control.setAttribute('aria-label', question);
        control.addEventListener('keydown', event => {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault(); control.click();
            }
        });
        control.addEventListener('click', () => {
            control.setAttribute('aria-expanded', String(content.style.display === 'block'));
        });
    });
    document.querySelectorAll('.flip-card').forEach(card => { card.tabIndex = 0; });
    if (sidebar) sidebar.addEventListener('keydown', event => {
        if (event.key !== 'Tab') return;
        const controls = Array.from(sidebar.querySelectorAll('a[href]'));
        const first = controls[0], last = controls[controls.length - 1];
        if (event.shiftKey && document.activeElement === first) {
            event.preventDefault(); last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
            event.preventDefault(); first.focus();
        }
    });
    window.matchMedia('(min-width:1101px)').addEventListener('change', event => {
        if (event.matches) hideSidebar(false);
    });
});
