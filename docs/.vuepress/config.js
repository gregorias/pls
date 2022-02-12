const packageInfo  = require('../../package.json');

module.exports = {
  lang: 'en-GB',
  title: 'pls Documentation',
  description: packageInfo.description,
  base: '/pls/',

  theme: '@vuepress/theme-default',
  themeConfig: {
    repo: packageInfo.repository.replace('github:', ''),
    docsBranch: 'docs',
    docsDir: 'docs',
  },
};
