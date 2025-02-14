<script setup>
import {getCurrentInstance, ref } from 'vue';
import { Button } from "@/components/ui/button"; // Adjust this path based on your Button component
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card"; // Adjust paths to your components as needed

</script>

<template>
  <div class="dark:bg-slate-900 bg-white min-h-[calc(100vh-4rem)]">

    
    <!-- Router View -->
    <div class="flex justify-center">
      <router-view></router-view>
    </div>
  </div>
</template>

<style scoped>
/* Add additional styling if necessary */
</style>
