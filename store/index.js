// store/index.js
export const state = () => ({
    user: null,
    token: null,
  });
  
  export const getters = {
    isAuthenticated(state) {
      return !!state.token; // Vérifie si l'utilisateur est authentifié
    },
    userRole(state) {
      return state.user?.role || 'guest'; // Par défaut, retourne 'guest'
    },
  };
  
  export const mutations = {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
    },
    logout(state) {
      state.user = null;
      state.token = null;
    },
  };
  
  export const actions = {
    login({ commit }, { user, token }) {
      commit('setUser', user);
      commit('setToken', token);
    },
    logout({ commit }) {
      commit('logout');
    },
  };
  