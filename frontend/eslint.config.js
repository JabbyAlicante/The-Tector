import globals from 'globals';
import pluginJs from '@eslint/js';

export default [
  {
    ignores: [
      'dist',
      'node_modules'
    ]
  },
  {
    languageOptions: { globals: globals.browser },
    rules: {
      'quotes': [2, 'single', { 'avoidEscape': true }]
    },
  },
  pluginJs.configs.recommended,
];