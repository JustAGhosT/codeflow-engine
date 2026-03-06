export default function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white/30 backdrop-blur-sm dark:border-slate-700 dark:bg-slate-900/30">
      <div className="mx-auto max-w-7xl px-6 py-8 text-center text-slate-600 dark:text-slate-400">
        <p>&copy; {new Date().getFullYear()} CodeFlow Engine. All rights reserved.</p>
      </div>
    </footer>
  );
}
