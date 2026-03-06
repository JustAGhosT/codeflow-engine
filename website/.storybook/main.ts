import type { StorybookConfig } from '@storybook/nextjs';

/**
 * Storybook Configuration
 * @audit DEBT-13 - Add Storybook for component documentation
 *
 * This configuration sets up Storybook for the Next.js App Router project.
 * Stories are located alongside components in the app/components directory.
 */
const config: StorybookConfig = {
  stories: [
    '../app/components/**/*.stories.@(js|jsx|mjs|ts|tsx)',
    '../stories/**/*.stories.@(js|jsx|mjs|ts|tsx)',
  ],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
  ],
  framework: {
    name: '@storybook/nextjs',
    options: {
      // Next.js App Router configuration
      builder: {
        useSWC: true,
      },
    },
  },
  staticDirs: ['../public'],
  docs: {
    autodocs: 'tag',
  },
  typescript: {
    reactDocgen: 'react-docgen-typescript',
  },
};

export default config;
