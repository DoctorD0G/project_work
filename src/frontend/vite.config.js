import {fileURLToPath, URL} from 'node:url';

import {defineConfig} from 'vite';
import vue from '@vitejs/plugin-vue';

import {quasar, transformAssetUrls} from '@quasar/vite-plugin';

export default defineConfig({
  plugins: [
    vue({
      template: {transformAssetUrls},
    }),
    quasar({
      sassVariables: 'cism-front-base/src/assets/styles/variables.scss',
    }),
  ],
  server: {
    watch: {
      usePolling: true,
    }
  },
  css: {
    devSourcemap: true,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
});
