import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import ThemeToggle from '../ThemeToggle';
import { ThemeProvider } from '../ThemeProvider';

// Wrapper component that provides ThemeProvider context
function renderWithTheme(component: React.ReactElement) {
  return render(<ThemeProvider>{component}</ThemeProvider>);
}

describe('ThemeToggle', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset localStorage mock
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue(null);
  });

  it('renders without crashing', () => {
    renderWithTheme(<ThemeToggle />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('displays theme label in button', () => {
    renderWithTheme(<ThemeToggle />);
    // Default theme should be 'system' which resolves to 'light' in tests
    expect(screen.getByRole('button')).toHaveAttribute(
      'aria-label',
      expect.stringContaining('System')
    );
  });

  it('cycles through themes when clicked', () => {
    renderWithTheme(<ThemeToggle />);
    const button = screen.getByRole('button');

    // Initial state is 'system', after click should be 'light'
    fireEvent.click(button);
    expect(button).toHaveAttribute(
      'aria-label',
      expect.stringContaining('Light')
    );

    // After another click should be 'dark'
    fireEvent.click(button);
    expect(button).toHaveAttribute(
      'aria-label',
      expect.stringContaining('Dark')
    );

    // After another click should be 'system'
    fireEvent.click(button);
    expect(button).toHaveAttribute(
      'aria-label',
      expect.stringContaining('System')
    );
  });

  it('has accessible title attribute', () => {
    renderWithTheme(<ThemeToggle />);
    const button = screen.getByRole('button');
    expect(button).toHaveAttribute('title', expect.stringContaining('Theme:'));
  });

  it('saves theme to localStorage when changed', () => {
    renderWithTheme(<ThemeToggle />);
    const button = screen.getByRole('button');

    fireEvent.click(button);
    expect(window.localStorage.setItem).toHaveBeenCalledWith('theme', 'light');
  });
});
