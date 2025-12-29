
export default function sidebar(root) {
  root.innerHTML = `
    <div class="sidebar">
      <button data-mode="spam">Spam</button>
      <button data-mode="fake">Fake News</button>
      <button data-mode="badwords">Inappropriate words</button>
    </div>
  `;
}