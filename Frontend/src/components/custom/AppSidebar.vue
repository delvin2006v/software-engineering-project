<script setup>
import { defineComponent, reactive } from 'vue';

import Sidebar from '@/components/ui/sidebar/Sidebar.vue';
import SidebarContent from '@/components/ui/sidebar/SidebarContent.vue';
import SidebarFooter from '@/components/ui/sidebar/SidebarFooter.vue';
import SidebarGroup from '@/components/ui/sidebar/SidebarGroup.vue';
import SidebarGroupContent from '@/components/ui/sidebar/SidebarGroupContent.vue';
import SidebarGroupLabel from '@/components/ui/sidebar/SidebarGroupLabel.vue';
import SidebarMenu from '@/components/ui/sidebar/SidebarMenu.vue';
import SidebarMenuButton from '@/components/ui/sidebar/SidebarMenuButton.vue';
import SidebarMenuItem from '@/components/ui/sidebar/SidebarMenuItem.vue';

import DropdownMenu from '@/components/ui/dropdown-menu/DropdownMenu.vue';
import DropdownMenuTrigger from '@/components/ui/dropdown-menu/DropdownMenuTrigger.vue';
import DropdownMenuContent from '@/components/ui/dropdown-menu/DropdownMenuContent.vue';
import DropdownMenuItem from '@/components/ui/dropdown-menu/DropdownMenuItem.vue';

import Home from '@/assets/icons/house.png';

// Menu items
const items = reactive([
  {
    title: 'Home',
    url: '/',
    icon: Home,
  },

  {
    title: 'Dashboard',
    url: '/dashboard',
    icon: Home,
  },
  {
    title: 'Courses',
    url: '#',
    icon: Home,
  },
  {
    title: 'Downloads',
    url: '#',
    icon: Home,
  },
  {
    title: 'Documents',
    url: '#',
    icon: Home,
  },
]);
</script>

<template>
  <Sidebar class="animated-sidebar">
    <SidebarContent>
      <SidebarGroup>
        <SidebarGroupLabel class="heading">IIT BS Degree</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem
              v-for="item in items"
              :key="item.title"
              class="animated-menu-item"
            >
              <SidebarMenuButton as-child>
                <router-link :to="item.url" class="flex items-center space-x-3 hover:menu-hover">
                  <img :src="item.icon" alt="" class="icon-size" />
                  <span class="menu-title">{{ item.title }}</span>
                </router-link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>

    <!-- Sidebar Footer -->
    <SidebarFooter>
      <SidebarMenu>
        <SidebarMenuItem>
          <DropdownMenu>
            <DropdownMenuTrigger as-child>
              <SidebarMenuButton class="footer-trigger">
                <User2 /> Username
                <ChevronUp class="ml-auto footer-chevron" />
              </SidebarMenuButton>
            </DropdownMenuTrigger>
            <DropdownMenuContent
              side="top"
              class="dropdown-menu w-[--radix-popper-anchor-width]"
            >
              <DropdownMenuItem class="dropdown-item">
                <span>Account</span>
              </DropdownMenuItem>
              <DropdownMenuItem class="dropdown-item">
                <span>Settings</span>
              </DropdownMenuItem>
              <DropdownMenuItem class="dropdown-item">
                <span>Sign out</span>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarMenuItem>
      </SidebarMenu>
    </SidebarFooter>
  </Sidebar>
</template>

<style>
.animated-sidebar {
  background: rgb(15 23 42 / var(--tw-bg-opacity, 1));
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
}
.animated-sidebar:hover {
  box-shadow: 4px 0 15px rgba(0, 0, 0, 0.2);
}

.heading {
  font-size: 22px;
  font-weight: bold;
  padding: 10px 20px;
  color: #fbfbfb;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.icon-size {
  width: 28px;
  height: 28px;
  object-fit: contain;
  transition: transform 0.3s ease;
}
.icon-size:hover {
  transform: scale(1.2);
}

.animated-menu-item {
  padding: 10px 15px;
  border-radius: 6px;
  transition: background-color 0.3s ease, transform 0.3s ease;
}
.animated-menu-item:hover {
  background-color: rgb(38, 46, 63);
  transform: translateX(5px);
}

.menu-hover {
  color: #555;
  font-weight: 500;
  transition: color 0.3s ease;
}
.menu-hover:hover {
  color: #000;
}

.footer-trigger {
  padding: 12px;
  display: flex;
  align-items: center;
  border-radius: 8px;
  transition: background-color 0.3s ease, transform 0.3s ease;
}
.footer-trigger:hover {
  background-color: rgb(38, 46, 63);
  transform: scale(1.05);
}

.footer-chevron {
  transition: transform 0.3s ease;
}
.footer-trigger:hover .footer-chevron {
  transform: rotate(180deg);
}

.dropdown-menu {
  background: rgb(38, 46, 63);
  border-radius: 8px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.dropdown-item {
  padding: 10px 15px;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.dropdown-item:hover {
  background-color: rgb(116, 117, 118);
  color: #000;
}

.menu-title {
  transition: color 0.3s ease;
}
.menu-title:hover {
  color: #e2e0e0;
}
</style>

