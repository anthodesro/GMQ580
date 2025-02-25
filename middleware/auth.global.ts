// auth.global.ts
export default defineNuxtRouteMiddleware((to, from) => {
    if (process.server) return; // Ne s'exécute pas côté serveur
  
    // Vérification du token dans localStorage ou sessionStorage
    const token = localStorage.getItem("token") || sessionStorage.getItem("token");
  
    // Si pas de token et tentative d'accès à une page protégée, redirige vers login
    if (!token && to.path !== "/auth/login") {
      return navigateTo("/auth/login");
    }
  });
  