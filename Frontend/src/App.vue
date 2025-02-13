<script setup>
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'

const store = useStore()
const route = useRoute()
</script>

<template>
  <div>
    <!-- Show navigation bar only if user is authenticated -->
    <nav v-if="store.state.isAuthenticated" class="bg-gray-800 text-white p-4 flex justify-between">
      <span class="text-xl">Dashboard</span>
      <button @click="store.dispatch('logout')" class="bg-red-500 px-4 py-2 rounded">
        Logout
      </button>
    </nav>

    <!-- Display dynamic pages based on route -->
    <router-view></router-view>
  </div>
</template>

<style scoped>
/* Add any custom styles if needed */
</style>
