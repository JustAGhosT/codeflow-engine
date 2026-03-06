import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";
import tsconfigPaths from "vite-tsconfig-paths";

const env = (globalThis as { process?: { env?: Record<string, string | undefined> } }).process?.env ?? {};
const host = env.TAURI_DEV_HOST;
const isTauriDebug = !!env.TAURI_DEBUG;
const buildMinify: false | "esbuild" = isTauriDebug ? false : "esbuild";

// https://vite.dev/config/
export default defineConfig(() => ({
  plugins: [react(), tsconfigPaths()],

  // Vite options tailored for Tauri development and only applied in `tauri dev` or `tauri build`
  //
  // 1. prevent Vite from obscuring rust errors
  clearScreen: false,
  // 2. tauri expects a fixed port, fail if that port is not available
  server: {
    port: 1420,
    strictPort: true,
    host: host || false,
    hmr: host
      ? {
        protocol: "ws",
        host,
        port: 1421,
      }
      : undefined,
    watch: {
      // 3. tell Vite to ignore watching `src-tauri`
      ignored: ["**/src-tauri/**"],
    },
  },

  // 3. to make use of `TAURI_DEBUG` and other env variables
  // https://tauri.app/v1/api/config#buildconfig.beforedevcommand
  envPrefix: ["VITE_", "TAURI_"],
  build: {
    // Tauri supports es2021
    target: env.TAURI_PLATFORM == "windows" ? "chrome105" : "safari13",
    // don't minify for debug builds
    minify: buildMinify,
    // produce sourcemaps for debug builds
    sourcemap: isTauriDebug,
    rollupOptions: {
      output: {
        manualChunks(id: string) {
          if (id.includes("node_modules/@rjsf") || id.includes("node_modules/ajv") || id.includes("node_modules/js-yaml")) {
            return "form-vendors";
          }
          if (id.includes("node_modules/react") || id.includes("node_modules/react-dom") || id.includes("node_modules/react-router-dom")) {
            return "react-vendors";
          }
        },
      },
    },
  },
  base: "./",
}));
