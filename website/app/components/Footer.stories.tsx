import type { Meta, StoryObj } from '@storybook/react';
import Footer from './Footer';

/**
 * Footer Component Stories
 * @audit DEBT-13 - Add Storybook for component documentation
 *
 * The Footer component displays the copyright notice with a backdrop blur effect.
 * It automatically updates the year and adapts to light/dark themes.
 */
const meta = {
  title: 'Components/Footer',
  component: Footer,
  tags: ['autodocs'],
  parameters: {
    layout: 'fullscreen',
  },
} satisfies Meta<typeof Footer>;

export default meta;
type Story = StoryObj<typeof meta>;

// Default footer (light mode)
export const Default: Story = {};

// Footer in context (full width)
export const InPageContext: Story = {
  render: () => (
    <div className="flex min-h-[400px] flex-col bg-slate-50 dark:bg-slate-900">
      <main className="flex-1 p-8">
        <p className="text-center text-slate-500">Page content area</p>
      </main>
      <Footer />
    </div>
  ),
};

// Footer showcase with both themes
export const ThemeComparison: Story = {
  render: () => (
    <div className="flex flex-col gap-8">
      <div>
        <p className="mb-2 text-sm font-medium text-slate-500">Light Mode</p>
        <div className="bg-slate-50">
          <Footer />
        </div>
      </div>
      <div className="dark">
        <p className="mb-2 text-sm font-medium text-slate-500">Dark Mode</p>
        <div className="bg-slate-900">
          <Footer />
        </div>
      </div>
    </div>
  ),
};
