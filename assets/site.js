(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.site-nav');

  if (menuButton && navigation) {
    menuButton.addEventListener('click', () => {
      const open = navigation.classList.toggle('is-open');
      menuButton.setAttribute('aria-expanded', String(open));
    });

    navigation.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        navigation.classList.remove('is-open');
        menuButton.setAttribute('aria-expanded', 'false');
      });
    });
  }

  const filters = document.querySelectorAll('[data-filter]');
  const courseCards = document.querySelectorAll('[data-audience]');
  const emptyState = document.querySelector('[data-filter-empty]');

  filters.forEach((button) => {
    button.addEventListener('click', () => {
      const selected = button.dataset.filter;
      let visible = 0;

      filters.forEach((item) => {
        const active = item === button;
        item.classList.toggle('is-active', active);
        item.setAttribute('aria-pressed', String(active));
      });

      courseCards.forEach((card) => {
        const show = selected === 'alle' || card.dataset.audience === selected;
        card.hidden = !show;
        if (show) visible += 1;
      });

      if (emptyState) emptyState.hidden = visible !== 0;
    });
  });
})();
