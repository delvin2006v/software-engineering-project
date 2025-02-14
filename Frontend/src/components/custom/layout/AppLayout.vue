<script>
    import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
    import AppSidebar from "@/components/custom/AppSidebar.vue";

    export default {
    name: "AppLayout",
    components: {
        SidebarProvider,
        SidebarTrigger,
        AppSidebar,
    },
    };
</script>

<template>
    <SidebarProvider>
      <AppSidebar />
      <main class="flex-1">
        <SidebarTrigger />
        <slot />
      </main>
    </SidebarProvider>
  </template>