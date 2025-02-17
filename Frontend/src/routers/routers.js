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
     component: () => import('@/views/Courses.vue'),
     meta: { requiresAuth: true } // Protect this route
   },
   {
    path: '/coursecontent',
    name: 'Content',
    component: () => import('@/views/CourseContent.vue'),
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
