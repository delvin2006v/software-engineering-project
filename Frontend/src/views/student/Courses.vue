<script setup>

import { ref, onMounted } from "vue";
import { useStore } from 'vuex';


// Importing UI components
import {
  Card,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const store = useStore();
console.log(store.state.user.token)
const courses = ref([]);


const fetchCourses = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/courses', {
      headers: {
        'Authentication-Token': store.state.user.token,
      },
    });

    if (response.data.status.success) {
      courses.value = response.data.data.courses.map(course => ({
        id: course.id,
        title: course.name,
        description: "No description available", // Prevents error if no description exists
      }));
    } else {
      console.error('Failed to fetch courses:', response.data.status.message);
    }
  } catch (error) {
    console.error('Error fetching courses:', error);
  }
};

onMounted(() => {
  fetchCourses();
});

</script>

<template>
  <div class="w-full p-6 main">
    <!-- Heading and CGPA Info -->
    <div class="mb-4">
      <h2 class="text-2xl font-bold text-gray-800">Current Courses</h2>
      <p class="text-lg text-gray-600 mt-1">CGPA till Now: <span class="font-semibold">8.5</span></p>
    </div>

    <!-- Course Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 w-fit">
      <router-link
        v-for="(course, index) in courses"
        :key="index"
        :to="'/coursecontent/' + course.id"
        class="block transition-transform transform hover:scale-105 hover:shadow-2xl duration-300"
      >
        <Card class="overflow-hidden shadow-lg rounded-lg">
          <img
            src="../../assets/images/AiCourse.jpeg"
            alt="Course Image"
            class="w-full h-48 object-cover"
          />
          <CardHeader>
            <CardTitle class="text-lg font-semibold">{{ course.title }}</CardTitle>
            <p class="text-sm text-gray-600">{{ course.description }}</p>
          </CardHeader>
          <CardFooter>
            <Button class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded">
              Visit
            </Button>
          </CardFooter>
        </Card>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.main {
  margin-top: 7vh;
  margin-bottom: 32vh;
  margin-left: 30px;
}
</style>
