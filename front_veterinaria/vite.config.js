// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      // --- ✨ AÑADE ESTA LÍNEA PARA SOLUCIONAR EL ERROR DE COMPILACIÓN ---
      'vue': 'vue/dist/vue.esm-bundler.js',
    }
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          'vendor': ['vue', 'vue-router', 'pinia', 'axios'],
          'ui': ['@headlessui/vue', '@heroicons/vue', 'feather-icons'],
        }
      }
    }
  }
})