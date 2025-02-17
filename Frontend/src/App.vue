<script setup>
import { useStore } from 'vuex'
import { useRoute } from 'vue-router'
import Navbar from "@/components/custom/layout/Navbar.vue";
import AppLayout from "@/components/custom/layout/AppLayout.vue";
import Footer from "@/components/custom/layout/Footer.vue";

const store = useStore()
const route = useRoute()
</script>

<template>
  <div>
    <div v-if="store.state.isAuthenticated">
      <Navbar v-if="store.state.isAuthenticated"/>

      <AppLayout v-if="store.state.isAuthenticated">
        <!-- <router-view />
        <Footer/> -->
      </AppLayout>

    </div>
    <div v-else>
      <router-view/>
    </div>
  </div>
</template>

<style scoped>
/* Add any custom styles if needed */
</style>

