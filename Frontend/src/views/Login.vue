<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

const store = useStore()
const router = useRouter()
const username = ref('')
const role = ref('')

const handleLogin = () => {
  if (username.value && role.value) {
    store.dispatch('login', {
      username: username.value,
      role: role.value
    })
    router.push('/dashboard') // Redirect to dashboard
  } else {
    alert('Please enter username and role!')
  }
}
</script>

<template>
  <Card class="w-96 mx-auto mt-20 p-6">
    <CardHeader>
      <CardTitle>Login</CardTitle>
      <CardDescription>Enter your details</CardDescription>
    </CardHeader>
    <CardContent>
      <input v-model="username" type="text" placeholder="Username" class="border p-2 w-full mb-2">
      <input v-model="role" type="text" placeholder="Role" class="border p-2 w-full mb-4">
    </CardContent>
    <CardFooter>
      <button @click="handleLogin" class="bg-blue-500 text-white p-2 w-full rounded">
        Login
      </button>
    </CardFooter>
  </Card>
</template>
