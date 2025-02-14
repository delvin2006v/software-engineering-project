<script setup>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import Navbar from '@/components/custom/layout/Navbar.vue';
import Sidebar from '@/components/custom/layout/Sidebar.vue';
import Content from '@/components/custom/layout/Content.vue';
import Footer from '@/components/custom/layout/Footer.vue';
import AppLayout from "@/components/custom/layout/AppLayout.vue";

const store = useStore()
const router = useRouter()

const handleLogout = () => {
  store.dispatch('logout')
  router.push('/')
}
</script>

<template>
  <Navbar></Navbar>
    <AppLayout>
        <!-- <Sidebar></Sidebar> -->
        <Content></Content>
        <Footer></Footer>
    </AppLayout>

  <div class="text-center mt-24">
    <h1 class="text-3xl font-bold">Welcome, {{ store.state.user.username }}</h1>
    <p class="text-lg">Role: {{ store.state.user.role }}</p>
    <button @click="handleLogout" class="mt-4 bg-red-500 text-white px-4 py-2 rounded">
      Logout
    </button>
  </div>
</template>
