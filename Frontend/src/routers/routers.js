import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store/vuex'

const routes = [
   {
     path: '/',
     name: 'Login',
     component: () => import('@/views/Login.vue')
   },
   {
     path: '/dashboard',
     name: 'Courses',
     component: () => import('@/views/student/Courses.vue'),
     meta: { requiresAuth: true } // Protect this route
   },

    {
    path: '/instructor-dashboard',
    name: 'Instructor Dashboard',
    component: () => import('@/views/InstructorDashboard.vue'),
    children:[
      {
        path: 'TA-course',
        component: () => import('@/views/TA/Tacourses.vue'),
      },
    ],
    meta: { requiresAuth: true } // Protect this route
    },

  {
    path: '/ta-dashboard',
    name: 'TA Dashboard',
    component: () => import('@/views/InstructorDashboard.vue'),
    children:[
      {
        path: 'TA-course',
        component: () => import('@/views/TA/Tacourses.vue'),
      },
      {
        path: 'TA-upload/:id',
        component: () => import('@/views/TA/Content-upload.vue'),
      },
    ],
    meta: { requiresAuth: true } // Protect this route
  },

  {
    path: '/completedcourse',
    name: 'ComplatedCourse',
    component: () => import('@/views/student/CompletedCourse.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/coursecontent/:id',  // Add :id as a dynamic parameter
    name: 'Content',
    component: () => import('@/views/student/CourseContent.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/document',
    name: 'Documnet',
    component: () => import('@/views/student/Document.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard to Protect Routes
router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth && !store.state.isAuthenticated) {
    next({ name: 'Login' }) // Redirect to Login if not authenticated
  } else {
    next()
  }
})

export default router
