// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Smoothie',
  tagline: 'make yo footage creamy!!',
  url: 'https://ctt.cx/',
  baseUrl: '/smoothie',
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  favicon: 'img/smoothie.png',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'couleur-tweak-tips', // Usually your GitHub org/user name.
  projectName: 'smoothie', // Usually your repo name.

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        // blog: {
        //   showReadingTime: true,
        //   // Please change this to your repo.
        //   // Remove this to remove the "edit this page" links.
        //   editUrl:
        //     'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        // },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Smoothie',
        logo: {
          alt: 'SmLogo',
          src: 'img/smoothie.png',
        },
        items: [
          {
            type: 'doc',
            docId: 'intro',
            position: 'left',
            label: 'Documentation',
          },
          // {
          //   to: '/blog',
          //   label: 'Blog',
          //   position: 'left'
          // },
          {
            href: 'https://github.com/couleur-tweak-tips/smoothie#installation',
            label: 'Install',
            position: 'right',
          },

          {
            href: 'https://github.com/couleur-tweak-tips/smoothie',
            label: 'Source',
            position: 'right',
          },

        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Repos',
            items: [
              {
                label: 'Smoothie',
                href: 'https://github.com/couleur-tweak-tips/Smoothie',
              },
              {
                label: 'Docusaurus directory',
                href: 'https://github.com/couleur-tweak-tips/Smoothie/tree/master/docusaurus',
              },
              {
                label: 'CTT Organization',
                href: 'https://github.com/couleur-tweak-tips',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'Discord',
                href: 'https://discordapp.com/invite/CTT',
              },
              {
                label: 'Twitter',
                href: 'https://twitter.com/couleurtweaks',
              },
            ],
          },
          {
            title: 'More',
            items: [
              {
                label: 'YouTube',
                href: 'https://youtube.com/Couleur',
              },
              {
                label: 'Telegram (contact)',
                href: 'https://t.me/Couleur',
              },
            ],
          },
        ],
        copyright: `A CTT project (GPL-3.0); built with Ducasaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
      },
    }),
};

module.exports = config;
