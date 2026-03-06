import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

/**
 * Button Component Stories
 * @audit DEBT-13 - Add Storybook for component documentation
 *
 * The Button component supports three variants (primary, secondary, outline)
 * and three sizes (sm, md, lg). It can render as a button element or a link.
 */
const meta = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'outline'],
      description: 'Visual variant of the button',
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Size of the button',
    },
    disabled: {
      control: 'boolean',
      description: 'Whether the button is disabled',
    },
    children: {
      control: 'text',
      description: 'Button content',
    },
  },
} satisfies Meta<typeof Button>;

export default meta;
type Story = StoryObj<typeof meta>;

// Primary variant stories
export const Primary: Story = {
  args: {
    variant: 'primary',
    size: 'md',
    children: 'Primary Button',
  },
};

export const PrimarySmall: Story = {
  args: {
    variant: 'primary',
    size: 'sm',
    children: 'Small Primary',
  },
};

export const PrimaryLarge: Story = {
  args: {
    variant: 'primary',
    size: 'lg',
    children: 'Large Primary',
  },
};

// Secondary variant stories
export const Secondary: Story = {
  args: {
    variant: 'secondary',
    size: 'md',
    children: 'Secondary Button',
  },
};

export const SecondarySmall: Story = {
  args: {
    variant: 'secondary',
    size: 'sm',
    children: 'Small Secondary',
  },
};

export const SecondaryLarge: Story = {
  args: {
    variant: 'secondary',
    size: 'lg',
    children: 'Large Secondary',
  },
};

// Outline variant stories
export const Outline: Story = {
  args: {
    variant: 'outline',
    size: 'md',
    children: 'Outline Button',
  },
};

export const OutlineSmall: Story = {
  args: {
    variant: 'outline',
    size: 'sm',
    children: 'Small Outline',
  },
};

export const OutlineLarge: Story = {
  args: {
    variant: 'outline',
    size: 'lg',
    children: 'Large Outline',
  },
};

// Disabled state
export const Disabled: Story = {
  args: {
    variant: 'primary',
    size: 'md',
    children: 'Disabled Button',
    disabled: true,
  },
};

// All variants showcase
export const AllVariants: Story = {
  args: {
    variant: 'primary',
    size: 'md',
    children: 'All Variants',
  },
  render: () => (
    <div className="flex flex-col gap-4">
      <div className="flex items-center gap-4">
        <Button variant="primary" size="sm">Primary SM</Button>
        <Button variant="primary" size="md">Primary MD</Button>
        <Button variant="primary" size="lg">Primary LG</Button>
      </div>
      <div className="flex items-center gap-4">
        <Button variant="secondary" size="sm">Secondary SM</Button>
        <Button variant="secondary" size="md">Secondary MD</Button>
        <Button variant="secondary" size="lg">Secondary LG</Button>
      </div>
      <div className="flex items-center gap-4">
        <Button variant="outline" size="sm">Outline SM</Button>
        <Button variant="outline" size="md">Outline MD</Button>
        <Button variant="outline" size="lg">Outline LG</Button>
      </div>
    </div>
  ),
};

// As link examples
export const AsInternalLink: Story = {
  args: {
    as: 'a',
    href: '/installation',
    variant: 'primary',
    size: 'md',
    children: 'Go to Installation',
  },
};

export const AsExternalLink: Story = {
  args: {
    as: 'a',
    href: 'https://github.com',
    isExternal: true,
    variant: 'outline',
    size: 'md',
    children: 'View on GitHub',
  },
};
