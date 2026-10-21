import { createStore } from "vuex";

const store = createStore({
  state() {
    return {
      user: JSON.parse(localStorage.getItem("user")) || {
        user_id: null,
        username: null,
        role: null,

        token: null,
      },
      isAuthenticated: localStorage.getItem("isAuthenticated") === "true",
    };
  },
  mutations: {
    SET_USER(state, payload) {
      state.user = {
        user_id: payload.user_id,
        username: payload.username,
        role: payload.role,
        token: payload.token,
      };
      state.isAuthenticated = true;

      // Store data in localStorage
      localStorage.setItem("user", JSON.stringify(state.user));
      localStorage.setItem("isAuthenticated", "true");
    },
    LOGOUT(state) {
      state.user = {
        user_id: null,
        username: null,
        role: null,
        token: null,
      };
      state.isAuthenticated = false;

      // Remove data from localStorage
      localStorage.removeItem("user");
      localStorage.removeItem("isAuthenticated");
    },

  },
  actions: {
    login({ commit }, userData) {
      commit("SET_USER", userData);
    },
    logout({ commit }) {
      commit("LOGOUT");
    },
  },
});

export default store;





// for storing details
// this.$store.dispatch('login', { username: 'JohnDoe', role: 'admin' });

// for ascessing
//  computed: {
//   username() {
//     return this.$store.state.user.username;
//   },
//   role() {
//     return this.$store.state.user.role;
//   }
// }

// for logout
// this.$store.dispatch('logout');


