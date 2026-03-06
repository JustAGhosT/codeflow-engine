import type { Meta, StoryObj } from '@storybook/react';
import ThemeToggle from './ThemeToggle';
import { ThemeProvider } from './ThemeProvider';

/**
 * ThemeToggle Component Stories
 * @audit DEBT-13 - Add Storybook for component documentation
 *
 * The ThemeToggle component provides a button that cycles through
 * light, dark, and system theme modes. It must be wrapped in ThemeProvider.
 */
const meta = {
  title: 'Components/ThemeToggle',
  component: ThemeToggle,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
  decorators: [
    (Story) => (
      <ThemeProvider>
        <Story />
      </ThemeProvider>
    ),
  ],
} satisfies Meta<typeof ThemeToggle>;

export default meta;
type Story = StoryObj<typeof meta>;

// Default toggle
export const Default: Story = {};

// Toggle in navigation context
export const InNavigation: Story = {
  render: () => (
    <ThemeProvider>
      <nav className="flex items-center justify-between rounded-lg border border-slate-200 bg-white/60 px-6 py-4 backdrop-blur-sm dark:border-slate-700 dark:bg-slate-800/60">
        <span className="font-semibold text-slate-900 dark:text-slate-50">
          CodeFlow
        </span>
        <div className="flex items-center gap-4">
          <a
            href="#"
            className="text-sm text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-50"
          >
            Docs
          </a>
          <a
            href="#"
            className="text-sm text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-50"
          >
            Pricing
          </a>
          <ThemeToggle />
        </div>
      </nav>
    </ThemeProvider>
  ),
  decorators: [
    (Story) => (
      <div className="w-[600px]">
        <Story />
      </div>
    ),
  ],
};

// Toggle states showcase (visual reference)
export const StatesShowcase: Story = {
  render: () => (
    <ThemeProvider>
      <div className="flex flex-col gap-4">
        <div>
          <p className="mb-2 text-sm font-medium text-slate-500">
            Interactive Toggle (click to cycle: Light → Dark → System)
          </p>
          <ThemeToggle />
        </div>
        <div className="mt-4 rounded-lg border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800">
          <p className="text-sm text-slate-600 dark:text-slate-400">
            The toggle cycles through three states:
          </p>
          <ul className="mt-2 list-inside list-disc text-sm text-slate-600 dark:text-slate-400">
            <li>☀️ Light - Forces light mode</li>
            <li>🌙 Dark - Forces dark mode</li>
            <li>🖥️ System - Follows OS preference</li>
          </ul>
        </div>
      </div>
    </ThemeProvider>
  ),
};
