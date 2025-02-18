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
  { 
    id: 1, 
    title: "Introduction to AI", 
    description: "Learn the basics of Artificial Intelligence.",
    grade: "A",
    completedTerm: "Fall 2023",
    level: "Degree"
  },
  { 
    id: 2, 
    title: "Web Development Bootcamp", 
    description: "Master frontend and backend web development.",
    grade: "B+",
    completedTerm: "Spring 2023",
    level: "Diploma"
  },
  { 
    id: 3, 
    title: "Data Science Essentials", 
    description: "Understand data processing and visualization.",
    grade: "A-",
    completedTerm: "Winter 2022",
    level: "Foundation"
  },
  { 
    id: 3, 
    title: "Data Science Essentials", 
    description: "Understand data processing and visualization.",
    grade: "A-",
    completedTerm: "Winter 2022",
    level: "Foundation"
  },
  { 
    id: 3, 
    title: "Data Science Essentials", 
    description: "Understand data processing and visualization.",
    grade: "A-",
    completedTerm: "Winter 2022",
    level: "Foundation"
  },
  { 
    id: 3, 
    title: "Data Science Essentials", 
    description: "Understand data processing and visualization.",
    grade: "A-",
    completedTerm: "Winter 2022",
    level: "Foundation"
  },
]);
</script>

<template>
  <div class="w-full p-6 main">
    <!-- Heading and CGPA Info -->
    <div class="mb-4">
      <h2 class="text-2xl font-bold text-gray-800">Completed Courses</h2> 
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
            class="w-full h-48 object-cover rounded"
          />
          <CardHeader>
            <CardTitle class="text-lg font-semibold">{{ course.title }}</CardTitle>
            <p class="text-sm text-gray-600">{{ course.description }}</p>
          </CardHeader>
          <div class="p-2 text-white-100 text-sm ml-5">
            <p><strong>Grade:</strong> {{ course.grade }}</p>
            <p><strong>Completed Term:</strong> {{ course.completedTerm }}</p>
            <p><strong>Course Level:</strong> {{ course.level }}</p>
          </div>
          <CardFooter>
            <Button class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded mt-6">
              Visit
            </Button>
          </CardFooter>
        </Card>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.main{
  margin-top: 7vh;
  margin-bottom: 32vh;
  margin-left: 30px;
}
</style>