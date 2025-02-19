<script setup>
import { ref } from "vue"
import { useStore } from 'vuex';

import {
  School,
  GalleryVerticalEnd,
  GraduationCap,
  CalendarDays,
  FolderKanban,
  NotebookPen,
  FileSearch,
  Presentation,
  AlignEndHorizontal 
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

//Getting role from store
const store = useStore();

let navForTA  = [
  {
      title: "Courses",
      url: "#",
      icon: NotebookPen, // Set to null if using a custom image
      isActive: true,
      items: [
        { title: "Your Courses", url: "/dashboard" },
        { title: "TA Courses", url: "/ta-dashboard/TA-course" },
      ],
      
    },
    {
      title :"Statistics",
      url:'#',
      icon: AlignEndHorizontal,
      items: [
        { title: "Student Statistics", url: "/dashboard" },
        { title: "TA", url: "/completedcourse" },
      ],
    }
]

let navForInstructor  = [
  {
      title: "Courses",
      url: "#",
      icon: NotebookPen, 
      isActive: true,
      items: [
        { title: "Courses", url: "/instructor-dashboard/TA-course" },
      ],
      
    },
    {
      title :"Statistics",
      url:'#',
      icon: AlignEndHorizontal,
      items: [
        { title: "Student Statistics", url: "/instructor-dashboard/TA-course" },
        { title: "TA", url: "/instructor-dashboard/TA-course" },
      ],
    }
]

let navForStudents = [
    {
      title: "Courses",
      url: "#",
      icon: NotebookPen, // Set to null if using a custom image
      isActive: true,
      items: [
        { title: "Current Course", url: "/dashboard" },
        { title: "Completed Course", url: "/completedcourse" },
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
        { title: "All Docs", url: "/document" },
        { title: "Submited Docs", url: "/document" },
      ],
    },
  ]
  let navMain = store.state.user.role === "Instructor" 
  ? navForInstructor 
  : store.state.user.role === "TA" 
    ? navForTA 
    : navForStudents;


// Sample data using ref
const data = ref({
  user: {
    name: "IITM",
    email: "m@IITM.com",
    avatar: "../../assets/images/iitm.jpg",
  },
  teams: [
    {
      name: "IITM BS Degree",
      logoUrl: 'src/assets/images/iitm.png',
      plan: "DataScience",
    },

  ],
  navMain: navMain,
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
