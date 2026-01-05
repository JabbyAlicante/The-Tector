
export default function sidebar(root) {
  root.innerHTML = `
    <div class="sidebar">
      <button class="spam-btn" data-mode="spam">Spam</button>
      <button class="fake-btn" data-mode="fake">Fake News</button>
      <button class="hate-btn" data-mode="badwords">Hate words</button>
    </div>
  `;
}