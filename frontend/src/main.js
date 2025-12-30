import SPA from './core/spa.js';
import The_TectorPage from "./pages/The-TectorPage.js";

import './styles/global.css';
import './styles/header.css';
import './styles/mainpage.css';
import './styles/contents.css';
import './styles/sidebar.css';

const app = new SPA({
  root: document.getElementById('app'),
  defaultRoute: The_TectorPage,
});

app.add('/', The_TectorPage);
app.handleRouteChanges();
