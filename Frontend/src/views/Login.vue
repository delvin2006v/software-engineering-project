<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const store = useStore()
const router = useRouter()
const username = ref('')
const role = ref('')
const errorMessage = ref('')

const handleLogin = () => {
  if (username.value && role.value) {
    store.dispatch('login', {
      username: username.value,
      role: role.value
    })
    router.push('/dashboard') // Redirect to dashboard
  } else {
    errorMessage.value = 'Please enter both Username and Role!'
  }
}
</script>

<template>
  <div class="flex min-h-screen flex-col justify-center px-6 py-12 lg:px-8 bg-gray-100">
    <div class="max-w-md w-full mx-auto bg-white shadow-lg rounded-lg p-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <img 
          class="mx-auto h-10 w-auto" 
          src="../assets//images/iitm.png" 
          alt="Your Company" 
        />
        <h2 class="mt-6 text-center text-2xl font-bold tracking-tight text-gray-900">
          Sign in to your account
        </h2>
      </div>

      <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-sm">
        <div class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-900">Username</label>
            <div class="mt-2">
              <input 
                v-model="username" 
                type="text" 
                id="username"
                placeholder="Enter your username"
                class="block w-full rounded-md border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:ring-2 focus:ring-indigo-600 focus:outline-none sm:text-sm transition-all duration-300"
              />
            </div>
          </div>

          <div>
            <label for="role" class="block text-sm font-medium text-gray-900">Role</label>
            <div class="mt-2">
              <input 
                v-model="role" 
                type="text" 
                id="role"
                placeholder="Enter your role"
                class="block w-full rounded-md border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:ring-2 focus:ring-indigo-600 focus:outline-none sm:text-sm transition-all duration-300"
              />
            </div>
          </div>

          <!-- Error Message -->
          <p v-if="errorMessage" class="text-red-500 text-sm">{{ errorMessage }}</p>

          <div>
            <button 
              @click="handleLogin" 
              class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-md hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2 transition-all duration-300"
            >
              Sign in
            </button>
          </div>
        </div>

        <p class="mt-8 text-center text-sm text-gray-500">
          Don't have an account?
          <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500 transition-all duration-300">
            Signup
          </a>
        </p>
      </div>
    </div>
  </div>
</template>
