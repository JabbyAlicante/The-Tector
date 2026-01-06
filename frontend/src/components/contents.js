export default function contents(root) {
  root.innerHTML = `
    <div class="contents">
      <div class="screen-title">
        > MESSAGE SCANNER
      </div>
      <input
        type="text"
        id="linkInput"
        class="link-input"
        placeholder="Input link..."
        hidden
      />
      <textarea
        id="detectorInput"
        placeholder="Paste text here..."></textarea>
      <button class="detect-btn" id="detectBtn">
        SCAN MESSAGE
      </button>
      <div class="result-box" id="resultBox" hidden>
        <span class="result-label">STATUS:</span>
        <span class="result-text" id="resultText">.......</span>
      </div>
      <div class="icons-integration">
        <span class="icon-label">INTEGRATIONS:</span>
        <a href="https://discord.com/oauth2/authorize?client_id=1456872953206800394&permissions=274877982720&integration_type=0&scope=bot" class="integration-btn" target="_blank">
          <i class="fa-brands fa-discord"></i> Discord
        </a>
        <a href="https://t.me/the_tector_bot" class="integration-btn">
          <i class="fa-brands fa-telegram"></i> Telegram
        </a>
      </div>
    </div>
  `;
}
