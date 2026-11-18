import { defineConfig } from 'vite'

// The frontend talks to the backend on a relative `/api` base so the same
// bundle works on Vercel (single origin, Services routing) and locally.
// During `npm run dev` this proxy forwards `/api/*` to the local FastAPI server.
export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:3000',
        changeOrigin: true
      }
    }
  }
})
