<script setup>
import { ref } from "vue";

// Importing UI components
import {
  Card,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";

const courses = ref([
  { id: 1, title: "Introduction to AI", description: "Learn the basics of Artificial Intelligence." },
  { id: 2, title: "Web Development Bootcamp", description: "Master frontend and backend web development." },
  { id: 3, title: "Data Science Essentials", description: "Understand data processing and visualization." },
]);

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
        :to="'/coursecontent'"
        class="block transition-transform transform hover:scale-105 hover:shadow-2xl duration-300"
      >
        <Card class="overflow-hidden shadow-lg rounded-lg">
          <img
            src="../assets/images/AiCourse.jpeg"
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
/* Add any custom styles if needed */
.main{
  margin-top: 7vh;
  margin-bottom: 32vh;
  margin-left: 30px;
}
</style>




<!-- :to="'/courses/details/' + course.id" -->
