<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

const store = useStore()
const router = useRouter()
const username = ref('')
const password = ref('')
const role = ref('')
const errorMessage = ref('')

const handleLogin = async () => {
  try {
    // Make API request
    const response = await axios.post('http://127.0.0.1:5000/user_login', {

      username: username.value,
      password: password.value
    });

    // Check if API response contains user data
    if (response.data.data && response.data.data.username && response.data.data.role) {
      const userData = {
        user_id: response.data.data.id,

        username: response.data.data.username,
        role: response.data.data.role,
        token: response.data.data.token // Assuming API returns a token
      };

      store.dispatch('login', userData);

      console.log(response.data.data)
      // Redirect user based on role
      if (response.data.data.role === 'ta') {
        router.push('/ta-dashboard');
      } else if (response.data.data.role === 'instructor') {

        router.push('/instructor-dashboard/TA-course');
      } else {
        router.push('/dashboard');
      }
    } else {
      errorMessage.value = 'Invalid response from server';
    }
  } catch (error) {
    console.error('Login error:', error);
    errorMessage.value = 'Login failed. Please check your credentials!';
  }
};



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
            <label for="password" class="block text-sm font-medium text-gray-900 mt-5">Password</label>
              <div class="mt-2">
<<<<<<< Updated upstream
=======
              <input 
                v-model="password" 
                type="text" 
                id="password"
                placeholder="Enter your password"
                class="block w-full rounded-md border-gray-300 px-3 py-2 text-gray-900 shadow-sm focus:ring-2 focus:ring-indigo-600 focus:outline-none sm:text-sm transition-all duration-300"
              />
            </div>
          </div>

          <div>
            <!-- <div class="mt-2">
            <label for="role" class="block text-sm font-medium text-gray-900">Role</label>
>>>>>>> Stashed changes
              <input 
                v-model="password" 
                type="text" 
                id="password"
                placeholder="Enter your password"
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
      </div>
    </div>
  </div>
</template>
