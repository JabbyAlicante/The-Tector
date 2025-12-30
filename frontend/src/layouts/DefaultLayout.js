export default function DefaultLayout(root) {
  const navigation = document.createElement('nav');
  navigation.id = 'navigation';

  const main = document.createElement('main');
  main.id = 'main';
  root.appendChild(navigation);
  root.appendChild(main);
  return { navigation, main };
}
