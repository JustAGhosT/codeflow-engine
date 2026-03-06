import type { Meta, StoryObj } from '@storybook/react';
import { FeatureCard } from './FeatureCard';

/**
 * FeatureCard Component Stories
 * @audit DEBT-13 - Add Storybook for component documentation
 *
 * The FeatureCard component displays product features with an icon,
 * title, and description. It supports both static and linked variants.
 */
const meta = {
  title: 'Components/FeatureCard',
  component: FeatureCard,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
  argTypes: {
    icon: {
      control: 'text',
      description: 'Emoji or icon to display',
    },
    title: {
      control: 'text',
      description: 'Card title',
    },
    description: {
      control: 'text',
      description: 'Card description',
    },
    href: {
      control: 'text',
      description: 'Optional link URL - if provided, card becomes clickable',
    },
    isExternal: {
      control: 'boolean',
      description: 'Whether the link opens in a new tab',
    },
  },
  decorators: [
    (Story) => (
      <div className="w-80">
        <Story />
      </div>
    ),
  ],
} satisfies Meta<typeof FeatureCard>;

export default meta;
type Story = StoryObj<typeof meta>;

// Static card (no link)
export const Static: Story = {
  args: {
    icon: '🤖',
    title: 'AI-Powered Analysis',
    description:
      'Intelligent code analysis using GPT-4 and Claude for deep insights into your codebase.',
  },
};

// Different icons
export const WithRocketIcon: Story = {
  args: {
    icon: '🚀',
    title: 'Lightning Fast',
    description:
      'Optimized for speed with incremental builds and intelligent caching.',
  },
};

export const WithSecurityIcon: Story = {
  args: {
    icon: '🔒',
    title: 'Enterprise Security',
    description:
      'SOC2 compliant with end-to-end encryption and role-based access control.',
  },
};

export const WithIntegrationIcon: Story = {
  args: {
    icon: '🔗',
    title: 'Seamless Integration',
    description:
      'Connect with GitHub, GitLab, Bitbucket, and your favorite development tools.',
  },
};

// Linked card (internal)
export const LinkedInternal: Story = {
  args: {
    icon: '📚',
    title: 'Documentation',
    description: 'Learn how to get the most out of CodeFlow with our comprehensive guides.',
    href: '/docs',
  },
};

// Linked card (external)
export const LinkedExternal: Story = {
  args: {
    icon: '💻',
    title: 'View Source',
    description: 'Check out our open-source components and contribute to the project.',
    href: 'https://github.com',
    isExternal: true,
  },
};

// Feature grid showcase
export const FeatureGrid: Story = {
  args: {
    icon: '🤖',
    title: 'Feature Grid',
    description: 'This story shows multiple feature cards in a grid.',
  },
  render: () => (
    <div className="grid max-w-3xl grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      <FeatureCard
        icon="🤖"
        title="AI Analysis"
        description="Intelligent code analysis powered by GPT-4."
      />
      <FeatureCard
        icon="🚀"
        title="Fast Builds"
        description="Optimized builds with intelligent caching."
      />
      <FeatureCard
        icon="🔒"
        title="Secure"
        description="Enterprise-grade security and compliance."
      />
    </div>
  ),
  decorators: [],
};
