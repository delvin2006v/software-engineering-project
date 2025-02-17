<script setup>
import { ref } from "vue"

import {
  School,
  GalleryVerticalEnd,
  GraduationCap,
  CalendarDays,
  FolderKanban,
  NotebookPen,
  FileSearch,
  Presentation
} from "lucide-vue-next"

import NavMain from "./nav-main.vue"
import NavProjects from "./nav-projects.vue"
import NavUser from "./nav-user.vue"
import TeamSwitcher from "./team-switcher.vue"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/components/ui/sidebar"

// Sample data using ref
const data = ref({
  user: {
    name: "shadcn",
    email: "m@example.com",
    avatar: "../../assets/images/iitm.jpg",
  },
  teams: [
    {
      name: "IITM BS Degree",
      logoUrl: 'src/assets/images/iitm.png',
      plan: "DataScience",
    },

  ],
  navMain: [
    {
      title: "Courses",
      url: "#",
      icon: NotebookPen, // Set to null if using a custom image
      isActive: true,
      items: [
        { title: "Current Course", url: "#" },
        { title: "Completed Course", url: "#" },
      ],
    },
    {
      title: "Projects",
      url: "#",
      icon: Presentation,
      items: [
        { title: "Current Project", url: "#" },
        { title: "Completed Project", url: "#" },
      ],
    },
    {
      title: "Documents Downloade",
      url: "#",
      icon: FileSearch,
      items: [
        { title: "Introduction", url: "#" },
        { title: "Get Started", url: "#" },
        { title: "Tutorials", url: "#" },
        { title: "Changelog", url: "#" },
      ],
    },
    {
      title: "Submited Docs",
      url: "#",
      icon: FolderKanban,
      items: [
        { title: "General", url: "#" },
        { title: "Team", url: "#" },
        { title: "Billing", url: "#" },
        { title: "Limits", url: "#" },
      ],
    },
  ],
  projects: [
    {
      name: "Hall Ticket & Exam Cities",
      url: "#",
      icon: School,
    },
    {
      name: "Academic Calendar",
      url: "#",
      icon: CalendarDays,
    },
    {
      name: "Certificates",
      url: "#",
      icon: GraduationCap,
    },
  ],
})
</script>

<template>
  <Sidebar collapsible="icon">
    <SidebarHeader>
      <TeamSwitcher :teams="data.teams" />
    </SidebarHeader>
    <SidebarContent>
      <NavMain :items="data.navMain" />
      <NavProjects :projects="data.projects" />
    </SidebarContent>
    <SidebarFooter>
      <NavUser :user="data.user" />
    </SidebarFooter>
    <SidebarRail />
  </Sidebar>
</template>
