/////////////////////////
/**
 * Theme Mode :: Components
 */
/////////////////////////

document.addEventListener('DOMContentLoaded', () => {
    const btn_theme_mode = document.querySelector('#btn_theme_mode');
    const icon = btn_theme_mode.querySelector('i');
    const span = btn_theme_mode.querySelector('span');

    function update_button(theme) {
        icon.className = theme === 'dark'
            ? 'bi bi-sun-fill fs-5'
            : 'bi bi-moon-stars-fill fs-5';
        if (span) span.textContent = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
    }

    // -------------------------

    const el = document.documentElement;
    const saved_theme = localStorage.getItem('theme') || 'light';

    el.setAttribute('data-bs-theme', saved_theme);
    update_button(saved_theme);

    btn_theme_mode.addEventListener('click', (e) => {
        e.preventDefault();
        let current_theme = el.getAttribute('data-bs-theme');
        let new_theme = current_theme === 'dark' ? 'light' : 'dark';

        el.setAttribute('data-bs-theme', new_theme);
        localStorage.setItem('theme', new_theme);
        update_button(new_theme);
    });
});

/////////////////////////
