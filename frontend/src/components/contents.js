export default function contents(root) {
  root.innerHTML = `
    <div class="contents">
      <div class="screen-title">
        > MESSAGE SCANNER
      </div>
      <textarea 
        id="detectorInput" 
        placeholder="Paste text or link here..."></textarea>
      <button class="detect-btn" id="detectBtn">
        SCAN MESSAGE
      </button>
      <div class="result-box" id="resultBox" hidden>
        <span class="result-label">STATUS:</span>
        <span class="result-text" id="resultText">Alert!! this is a Spam</span>
      </div>
      <div class="icons-integration">
        <span class="icon-label">INTEGRATIONS:</span>
        <a href="discord://discordapp.com/channels/@me" class="integration-btn">
            <i class="fa-brands fa-discord"></i> Discord
        </a>
        <a href="tg://resolve?domain=YourTelegramUsername" class="integration-btn">
            <i class="fa-brands fa-telegram"></i> Telegram
        </a>
      </div>
    </div>
  `;
}
