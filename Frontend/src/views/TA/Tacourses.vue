<script setup>
import { ref ,onBeforeMount} from "vue";
import axios from 'axios'
import {useStore} from 'vuex'

// Importing UI components
import {
  Card,
  CardHeader,
  CardTitle,
  CardFooter,
} from "@/components/ui/card";
const store = useStore()
const userCourses = ref([]);

async function AllCourses(){
const response = await axios.get('http://127.0.0.1:5000/courses',{
    headers: {
        'Authentication-Token': store.state.user.token,
      },
  })
  userCourses.value = response.data.data.courses

}
onBeforeMount(AllCourses)

</script>

<template>
  <div class="w-full p-6 main">
    <!-- Heading and CGPA Info -->
    <div class="mb-4">
      <h2 class="text-2xl font-bold text-gray-800">Courses as TA</h2>
    </div>

    <!-- Course Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 w-fit">
      <router-link
        v-for="(course, index) in userCourses"
        :key="index"
        :to="'/ta-dashboard/TA-upload/'+course.id"
        class="block transition-transform transform hover:scale-105 hover:shadow-2xl duration-300"
      >
        <Card class="overflow-hidden shadow-lg rounded-lg">
          <img
            src="../../assets/images/AiCourse.jpeg"
            alt="Course Image"
            class="w-full h-48 object-cover"
          />
          <CardHeader>
            <CardTitle class="text-lg font-semibold">{{ course.name }}</CardTitle>
            <!-- <p class="text-sm text-gray-600">{{ course.description }}</p> -->
          </CardHeader>
          <CardFooter>
            <Button class="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded">
              Navigate to Upload
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
