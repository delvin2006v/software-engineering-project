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
    if(role.value =='TA'){
      router.push('/dashboard')
    } else if (role.value === 'Instructor') {
      router.push('/instructor-dashboard/TA-course'); // Redirect TA to Tadashboard
    } else{

      router.push('/dashboard') // Redirect to dashboard
    }
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
            <!-- <div class="mt-2">
            <label for="role" class="block text-sm font-medium text-gray-900">Role</label>
              <input 
                v-model="role" 
                type="text" 
                id="role"
                placeholder="Enter your role"
                class="block w-full rounded-md border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:ring-2 focus:ring-indigo-600 focus:outline-none sm:text-sm transition-all duration-300"
              />
            This componenet has been changed by Kishar / time 5:29 date 18-02-25
            </div>  -->
            <label for="countries" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Role</label>
            <select v-model="role"  id="countries" class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500">
              <option selected>Choose a role</option>
              <option value="Student">Student</option>
              <option value="TA">TA</option>
              <option value="Instructor">Instructor</option>
            </select>
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
      </div>
    </div>
  </div>
</template>
