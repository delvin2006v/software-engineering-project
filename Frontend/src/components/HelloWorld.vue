<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

</script>

<template>
  <h1 class="font-semibold text-4xl shadow-xl p-2">{{ msg }}</h1>
  <br>
  <a class="hover:text-blue-700 hover:underline text-2xl" href="https://vite.dev/guide/">Vite</a><br>
  <a class="hover:text-blue-700 hover:underline text-2xl" href="https://vuejs.org/guide/introduction.html">Vue 3</a><br>
  <a class="hover:text-blue-700 hover:underline text-2xl" href="https://ui.shadcn.com/docs">Shadcn</a><br>
</template>

<style scoped>

</style>