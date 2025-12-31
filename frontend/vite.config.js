import { defineConfig } from "vite";

export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      "/spam": {
        target: "http://localhost:5000",
        changeOrigin: true
      },
      "/api": {
        target: "http://172.20.207.196:8000",
        changeOrigin: true
      }
    }
  }
});
