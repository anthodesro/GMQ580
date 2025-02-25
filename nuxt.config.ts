export default defineNuxtConfig({
  ssr: false,
  typescript: {
    shim: false,
  },
  app: {
    baseURL: '/solvia/', // Assurez-vous que cela est correct
    buildAssetsDir: 'assets', // Vérifiez que la structure des assets est correcte
    head: {
      title: "Solvia",
    },
  },
  build: {
    transpile: ["vuetify"],
  },
  nitro: {
    serveStatic: true,
  },
  sourcemap: { server: false, client: false },
  devServerHandlers: [],
});
