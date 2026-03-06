/**
 * Creates a debounced version of a function that delays invoking the function
 * until after `delay` milliseconds have elapsed since the last time the
 * debounced function was invoked.
 *
 * @param fn - The function to debounce
 * @param delay - The number of milliseconds to delay
 * @returns A debounced version of the function with a cancel method
 */
export function debounce<T extends (...args: Parameters<T>) => void>(
  fn: T,
  delay: number
): T & { cancel: () => void } {
  let timeoutId: ReturnType<typeof setTimeout> | null = null;

  const debounced = ((...args: Parameters<T>) => {
    if (timeoutId !== null) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => {
      fn(...args);
      timeoutId = null;
    }, delay);
  }) as T & { cancel: () => void };

  debounced.cancel = () => {
    if (timeoutId !== null) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
  };

  return debounced;
}
