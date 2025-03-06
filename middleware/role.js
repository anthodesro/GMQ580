export default defineNuxtRouteMiddleware((to, from) => {
  if (process.server) return; // Empêche l'exécution côté serveur, sessionStorage n'est pas disponible

  const token = sessionStorage.getItem('token') || localStorage.getItem('token'); // Récupère le token (sessionStorage ou localStorage)
  const userRole = sessionStorage.getItem('role') || localStorage.getItem('role'); // Récupère le rôle de l'utilisateur (sessionStorage ou localStorage)

  // Si aucun token ou rôle n'est trouvé, redirection vers la page de login
  if (!token || !userRole) {
    return navigateTo('/auth/login');
  }

  try {
    // Décodage du token (si c'est un JWT)
    const decodedToken = JSON.parse(atob(token.split('.')[1])); // Décoder le payload du token

    // Vérification de l'expiration du token
    if (decodedToken.exp * 1000 < Date.now()) {
      sessionStorage.removeItem('token'); // Supprimer le token expiré
      sessionStorage.removeItem('role');  // Supprimer le rôle pour éviter les incohérences
      localStorage.removeItem('token'); // Supprimer le token expiré du localStorage
      localStorage.removeItem('role');  // Supprimer le rôle pour éviter les incohérences
      return navigateTo('/auth/login'); // Redirection vers login
    }
  } catch (error) {
    console.error('Erreur de décryptage du token ou token invalide :', error);
    sessionStorage.removeItem('token'); // Nettoyer si token invalide
    sessionStorage.removeItem('role');
    localStorage.removeItem('token'); // Nettoyer dans localStorage aussi
    localStorage.removeItem('role');
    return navigateTo('/auth/login'); // Redirection vers login
  }

  // Cas spécifique pour la page login (si l'utilisateur est déjà connecté, rediriger vers le tableau de bord approprié)
  if (to.path === '/auth/login' && token && userRole) {
    if (userRole === 'admin') {
      return navigateTo('/dashboard/admin');
    } else if (userRole === 'gestio') {
      return navigateTo('/dashboard/gestio');
    } else if (userRole === 'user') {
      return navigateTo('/dashboard/user');
    }
  }

  // Cas spécifique pour la page index redirection vers le tableau de bord approprié
  if (to.path === '/') {
    if (userRole === 'admin') {
      return navigateTo('/dashboard/admin');
    } else if (userRole === 'gestio') {
      return navigateTo('/dashboard/gestio');
    } else if (userRole === 'user') {
      return navigateTo('/dashboard/user');
    }
  }

    // Cas spécifique pour la page index redirection vers le tableau de bord approprié
    if (to.path === '/') {
      if (userRole === 'admin') {
        return navigateTo('/dashboard/admin');
      } else if (userRole === 'gestio') {
        return navigateTo('/dashboard/gestio');
      } else if (userRole === 'user') {
        return navigateTo('/dashboard/user');
      }
    }

  // Cas spécifique pour le tableau de bord admin
  if (to.path === '/dashboard/admin') {
    if (userRole !== 'admin') {
      return navigateTo('/auth/Unauthorized'); // Redirige vers le tableau de bord si l'utilisateur n'est pas admin
    }
  }

  // Cas spécifique pour le tableau de bord gestio
  if (to.path === '/dashboard/gestio') {
    if (userRole !== 'gestio') {
      return navigateTo('/auth/Unauthorized'); // Redirige vers le tableau de bord si l'utilisateur n'est pas admin
    }
  }

  // Cas spécifique pour la page configuration de la section projtes
  if (to.path === '/projet/config') {
    if (userRole !== 'gestio' && userRole !== 'admin') {
      return navigateTo('/auth/Unauthorized'); // Redirige vers le tableau de bord si l'utilisateur n'est pas admin
    }
  }

  // Cas spécifique pour la page configuration de la section Admin
  if (to.path === '/admin/config') {
    if (userRole !== 'admin') {
      return navigateTo('/auth/Unauthorized'); // Redirige vers le tableau de bord si l'utilisateur n'est pas admin
    }
  }
  
  // Cas spécifique pour la page configuration de la section Admin
  if (to.path === '/admin/config') {
    if (userRole !== 'admin') {
      return navigateTo('/auth/Unauthorized'); // Redirige vers le tableau de bord si l'utilisateur n'est pas admin
    }
  }

  // Cas spécifique pour le tableau de bord user
  if (to.path === '/dashboard/user') {
    if (userRole !== 'user' && userRole !== 'admin') {
      return navigateTo('/auth/Unauthorized'); // Redirige vers la page Unauthorized si l'utilisateur n'est ni admin ni user
    }
}
});
