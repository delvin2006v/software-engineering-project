<script setup>
import { MoonIcon, SunIcon } from '@radix-icons/vue';
import { ref, onMounted } from 'vue';

// Initialize the dark mode state
const isDark = ref(false);


// Check if the user has already selected dark mode in localStorage and apply it otherwise use system's settings
onMounted(() => {
  const storedTheme = window.localStorage.getItem('theme');
  if (storedTheme === null) {
    isDark.value = window.matchMedia('(prefers-color-scheme: dark)').matches; // prefers-color-scheme will look at os level not browser level.
  } else {
    isDark.value = storedTheme === 'dark';
  }

  if (isDark.value) {
    document.documentElement.classList.add('dark');
  }
});

// Toggle dark mode with updating the document's class list and localStorage
const toggleDarkMode = () => {
  document.documentElement.classList.toggle('dark');
  window.localStorage.setItem('theme', isDark.value ? 'light' : 'dark');
  isDark.value = !isDark.value;
};
</script>


<template>
    <div class="p-4">
        <button @click="toggleDarkMode"
                class="p-2 rounded-full"
                :class="isDark ? 'bg-slate-50 text-slate-950' : 'bg-slate-800 text-slate-50'">
                <SunIcon v-if="isDark"></SunIcon>
                <MoonIcon v-else></MoonIcon>
        </button>
   </div>
</template>


<style scoped>
    
</style>