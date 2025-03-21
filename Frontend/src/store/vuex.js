import { createStore } from 'vuex'

const store = createStore({
  state () {
    return {
      user: {
        username: null,
        role: null,
        token: null
      },
      isAuthenticated: false,
      token: null

    }
  },
  mutations: {
    SET_USER (state, payload) {
      state.user.username = payload.username
      state.user.role = payload.role
      state.user.token = payload.token
      state.isAuthenticated = true
    },
    LOGOUT (state) {
      state.user.username = null
      state.user.role = null
      state.user.token = null
      state.isAuthenticated = false
    }
  },
  actions: {
    login ({ commit }, userData) {
      commit('SET_USER', userData)
    },
    logout ({ commit }) {
      commit('LOGOUT')
    }
  }
})

export default store




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


