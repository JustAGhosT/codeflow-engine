import type { Preview } from '@storybook/react';
import '../app/globals.css';

/**
 * Storybook Preview Configuration
 * @audit DEBT-13 - Add Storybook for component documentation
 *
 * This file configures the preview iframe where stories are rendered.
 * It imports global CSS and sets up decorators for theme support.
 */
const preview: Preview = {
  parameters: {
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        {
          name: 'light',
          value: '#f8fafc',
        },
        {
          name: 'dark',
          value: '#0f172a',
        },
      ],
    },
    layout: 'centered',
  },
  globalTypes: {
    theme: {
      description: 'Global theme for components',
      defaultValue: 'light',
      toolbar: {
        title: 'Theme',
        icon: 'circlehollow',
        items: ['light', 'dark'],
        dynamicTitle: true,
      },
    },
  },
  decorators: [
    (Story, context) => {
      const theme = context.globals.theme;
      // Apply theme class to story container
      return (
        <div className={theme === 'dark' ? 'dark' : ''}>
          <div className="p-4 bg-slate-50 dark:bg-slate-900">
            <Story />
          </div>
        </div>
      );
    },
  ],
};

export default preview;
