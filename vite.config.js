import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import ViteYaml from '@modyfi/vite-plugin-yaml'
import path from 'path'

export default defineConfig({
  base: '/gig-ography/',
  plugins: [react(), tailwindcss(), ViteYaml()],
  resolve: {
    alias: { '@': path.resolve(__dirname, './src') }
  }
})
