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

      <div class="badwords-instructions" id="badwordsInstructions" style="display: none;">
        <div class="instruction-page" id="instructionPage0">
          <h3>Telegram Setup</h3>
          <ol>
            <li>Open Telegram.</li>
            <li>Search for the bot <strong>@HateSpeechDTCTR_bot</strong>.</li>
            <li>Start the bot.</li>
            <li>Add the bot to your group.</li>
            <li>Make sure the bot is set as an admin for it to work properly.</li>
          </ol>
          <p><em>Note: The bot cannot mute group owners.</em></p>
        </div>
        <div class="instruction-page" id="instructionPage1" style="display: none;">
          <h3>Discord Setup</h3>
          <ol>
            <li>Open Discord.</li>
            <li>Go to your server settings.</li>
            <li>Invite the bot using the Discord integration link.</li>
            <li>Make sure the bot has proper permissions.</li>
          </ol>

          <p><em>Note: Only admins can manage the bot permissions.</em></p>

          <h4>What the Bot Does</h4>
          <ul>
            <li>Automatically scans messages</li>
            <li>Detects profanity, hate speech, slurs, and violent language</li>
            <li>Removes violating messages instantly</li>
          </ul>

          <h4>If You Break the Rules</h4>
          <ul>
            <li>Your message will be deleted</li>
            <li>You’ll receive a warning in the channel</li>
            <li>Repeated violations result in a timeout or mute</li>
            <li>Severe or repeated hate speech may lead to a ban</li>
          </ul>

          <h4>Muted Users</h4>
          <ul>
            <li>Cannot send messages</li>
            <li>Mutes expire automatically</li>
          </ul>

        </div>
        <div class="instruction-navigation">
          <button id="prevBtn" class="prev-btn">&lt;</button>
          <button id="nextBtn" class="next-btn">&gt;</button>
        </div>
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

  const pages = document.querySelectorAll(".instruction-page");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  let currentPage = 0;

  function showPage(index) {
    pages.forEach((page, i) => {
      page.style.display = i === index ? "block" : "none";
    });
    prevBtn.disabled = index === 0;
    nextBtn.disabled = index === pages.length - 1;
  }

  prevBtn.addEventListener("click", () => {
    if (currentPage > 0) {
      currentPage--;
      showPage(currentPage);
    }
  });

  nextBtn.addEventListener("click", () => {
    if (currentPage < pages.length - 1) {
      currentPage++;
      showPage(currentPage);
    }
  });

  showPage(currentPage);
}
