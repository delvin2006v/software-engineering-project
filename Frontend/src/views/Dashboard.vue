<script setup>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const handleLogout = () => {
  store.dispatch('logout')
  router.push('/')
}
</script>

<template>
  <div class="text-center mt-24">
    <h1 class="text-3xl font-bold">Welcome, {{ store.state.user.username }}</h1>
    <p class="text-lg">Role: {{ store.state.user.role }}</p>
    <button @click="handleLogout" class="mt-4 bg-red-500 text-white px-4 py-2 rounded">
      Logout
    </button>
  </div>
</template>
