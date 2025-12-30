class SPA {
  routes = [];

  constructor(config = {}) {
    this.context = {
      root: config?.root || document.getElementById('app'),
      redirect: this.redirect.bind(this),
    };

    this.defaultRoute = {
      key: '*',
      callback: (config?.defaultRoute || (() => {})).bind(this.context),
    };
  }

  add(path, cb) {
    this.routes.push({
      key: path,
      callback: cb.bind(this.context),
    });
  }

  get(path) {
    const route = this.routes.find(r => (r.key instanceof RegExp && r.key.test(path)) || r.key === path);
    return route || this.defaultRoute;
  }

  execute(path) {
    const route = this.get(path);
    try {
      route?.callback();
    } catch (error) {
      console.error('Error executing route callback:', error);
    }
  }

  navigate(path) {
    history.pushState({}, '', path);
    this.execute(path);
  }

  redirect(url) {
    history.pushState({}, '', url);
    this.execute(window.location.pathname);
  }

  handleRouteChanges() {
    window.addEventListener('popstate', () => {
      this.execute(window.location.pathname);
    });

    document.addEventListener('click', (e) => {
      const link = e.target.closest('a');
      if (link && link.getAttribute('href')?.startsWith('/')) {
        e.preventDefault();
        this.navigate(link.getAttribute('href'));
      }
    });

    this.execute(window.location.pathname);
  }
}

export default SPA;
