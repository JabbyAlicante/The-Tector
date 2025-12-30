import contents from "./contents.js";
import sidebar from "./sidebar.js";
import { setupSidebarMode } from "./sidebarMode.js";
import { setupScanHandler } from "./scanHandler.js";

export default function mainpage(root) {
  root.innerHTML = `
    <div class="mainpage">

      <div class="sky">
      <div class="cloud cloud1"></div>
      <div class="cloud cloud2"></div>
      <div class="cloud cloud3"></div>
    </div>
      <section class="sidebar-section"></section>
      <section class="content-section"></section>
    </div>
  `;

  contents(root.querySelector(".content-section"));
  sidebar(root.querySelector(".sidebar-section"));

  setupSidebarMode();
  setupScanHandler();

  const sky = root.querySelector(".sky");
  for (let i = 0; i < 10; i++) {
    const cloud = document.createElement("div");
    cloud.classList.add("cloud");
    cloud.style.top = `${Math.random() * 80}vh`;
    cloud.style.left = `${-Math.random() * 100}px`;
    cloud.style.animationDuration = `${30 + Math.random() * 40}s`;
    sky.appendChild(cloud);
  }


}
