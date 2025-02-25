// middleware/role.js
export default function ({ store, redirect }) {
  // Récupère le rôle de l'utilisateur depuis Vuex ou localStorage
  const userRole = store.state.user?.role || localStorage.getItem('role');

  // Vérifie si l'utilisateur a un rôle valide
  if (!userRole) {
    return redirect('/auth/login'); // Si aucun rôle n'est trouvé, redirige vers la page de login
  }

  // Redirection en fonction du rôle
  if (userRole === 'admin') {
    return redirect('/admin/dashboard');
  } else if (userRole === 'gestio') {
    return redirect('/gestio/dashboard');
  } else if (userRole === 'user') {
    return redirect('/dashboard/index');
  } else {
    return redirect('/auth/login'); // Si rôle invalide, redirige vers login
  }
}
