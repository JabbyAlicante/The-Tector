import contents from "./contents.js";
import sidebar from "./sidebar.js";
import { setupSidebarMode } from "./sidebarMode.js";
import { setupScanHandler } from "./scanHandler.js";

export default function mainpage(root) {
  root.innerHTML = `
    <div class="mainpage">
      <section class="sidebar-section"></section>
      <section class="content-section"></section>
    </div>
  `;

  contents(root.querySelector(".content-section"));
  sidebar(root.querySelector(".sidebar-section"));

  setupSidebarMode();
  setupScanHandler();
}
