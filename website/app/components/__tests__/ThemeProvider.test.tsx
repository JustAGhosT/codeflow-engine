import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, act } from '@testing-library/react';
import { ThemeProvider, useTheme } from '../ThemeProvider';

// Test component that exposes theme context
function ThemeConsumer() {
  const { theme, resolvedTheme, setTheme } = useTheme();
  return (
    <div>
      <span data-testid="theme">{theme}</span>
      <span data-testid="resolved">{resolvedTheme}</span>
      <button onClick={() => setTheme('dark')}>Set Dark</button>
      <button onClick={() => setTheme('light')}>Set Light</button>
      <button onClick={() => setTheme('system')}>Set System</button>
    </div>
  );
}

describe('ThemeProvider', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset localStorage mock
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue(null);
    (window.localStorage.setItem as ReturnType<typeof vi.fn>).mockImplementation(() => {});
    // Reset document classes
    document.documentElement.classList.remove('light', 'dark');
  });

  it('provides default theme context', () => {
    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    expect(screen.getByTestId('theme')).toHaveTextContent('system');
    expect(screen.getByTestId('resolved')).toHaveTextContent('light');
  });

  it('loads saved theme from localStorage', () => {
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue('dark');

    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    expect(screen.getByTestId('theme')).toHaveTextContent('dark');
  });

  it('ignores invalid theme values in localStorage', () => {
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockReturnValue('invalid-theme');

    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    // Should fall back to default 'system'
    expect(screen.getByTestId('theme')).toHaveTextContent('system');
  });

  it('updates theme when setTheme is called', () => {
    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    act(() => {
      screen.getByText('Set Dark').click();
    });

    expect(screen.getByTestId('theme')).toHaveTextContent('dark');
    expect(window.localStorage.setItem).toHaveBeenCalledWith('theme', 'dark');
  });

  it('throws error when useTheme is used outside provider', () => {
    // Suppress console.error for this test
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    expect(() => {
      render(<ThemeConsumer />);
    }).toThrow('useTheme must be used within a ThemeProvider');

    consoleSpy.mockRestore();
  });

  it('applies theme class to document element', () => {
    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    // After mount, should apply resolved theme class
    expect(document.documentElement.classList.contains('light')).toBe(true);

    act(() => {
      screen.getByText('Set Dark').click();
    });

    expect(document.documentElement.classList.contains('dark')).toBe(true);
    expect(document.documentElement.classList.contains('light')).toBe(false);
  });
});

describe('ThemeProvider localStorage error handling', () => {
  it('handles localStorage.getItem throwing an error', () => {
    (window.localStorage.getItem as ReturnType<typeof vi.fn>).mockImplementation(() => {
      throw new Error('localStorage is disabled');
    });

    // Should not throw, should fall back gracefully
    expect(() => {
      render(
        <ThemeProvider>
          <ThemeConsumer />
        </ThemeProvider>
      );
    }).not.toThrow();

    // Should use default theme
    expect(screen.getByTestId('theme')).toHaveTextContent('system');
  });

  it('handles localStorage.setItem throwing an error', () => {
    (window.localStorage.setItem as ReturnType<typeof vi.fn>).mockImplementation(() => {
      throw new Error('QuotaExceededError');
    });

    // Suppress console.error for this test
    const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    render(
      <ThemeProvider>
        <ThemeConsumer />
      </ThemeProvider>
    );

    // Should not throw when setting theme
    expect(() => {
      act(() => {
        screen.getByText('Set Dark').click();
      });
    }).not.toThrow();

    // Theme should still update in memory
    expect(screen.getByTestId('theme')).toHaveTextContent('dark');

    consoleSpy.mockRestore();
  });
});
