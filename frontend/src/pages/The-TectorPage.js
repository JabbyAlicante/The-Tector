import header from "../components/header.js";
import mainpage from "../components/mainpage.js";
import DefaultLayout from "../layouts/DefaultLayout.js";

export default function The_TectorPage() {
  const { navigation, main } = DefaultLayout(this.root);

  header(navigation);
  mainpage(main);
}
