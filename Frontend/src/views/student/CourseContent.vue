<script setup>
import { ref, computed, onMounted, onBeforeMount } from 'vue';
import { Disclosure, DisclosureButton } from '@headlessui/vue';
import { ChevronDown, ChevronRight, Play, BookOpen, ClipboardCheck, Pencil, Menu } from 'lucide-vue-next';
import Aibot from './Aibot.vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';

const route = useRoute();
const store = useStore();
const isSidebarOpen = ref(true);

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value;
};


const courseId = route.params.id;
let is_data_fetched = ref(false)
let courseContent = ref([]);
let selectedContent = ref({});
const contentType = ref("graded")

let expandedWeeks = ref([1]);

// this is for expanded week chnages
function updateExpandedWeeks(newWeek) {
  expandedWeeks.value = [newWeek];
}

// function for change

function transformCourseData(input) {
    const result = [];
    
    for (const week of input) {
        const transformedWeek = {
            week: week.id,
            title: week.title,
            lectures: [],
            practiceAssignments: [],
            gradedAssignments: []
        };
        
        for (const item of week.items || []) {
            if (item.type === "lecture") {
                transformedWeek.lectures.push({
                    id: item.id,
                    title: item.title,
                    videoId: item.url?.split('v=')[1] || item.url?.split('/').pop() || ""
                });
            } else if (item.type === "practice-assignment") {
                transformedWeek.practiceAssignments.push({
                    id: item.id,
                    title: item.title,
                    questions: item.questions.map(question => ({
                        text: question.question,
                        options: question.options || [],
                        correctAnswer: (question.answer && question.answer.length > 0 && question.options) 
                            ? question.options.indexOf(question.answer[0]) 
                            : -1 // Default to -1 if no valid answer is found
                    }))
                });
            } else if (item.type === "programming-assignment") {
                transformedWeek.gradedAssignments.push({
                    id: item.id,
                    title: item.title,
                    questions: [{
                        text: item.question,
                        options: item.cases?.map(c => c.output) || [],
                        correctAnswer: 0
                    }]
                });
            }
        }
        
        result.push(transformedWeek);
    }
    
    return result;
}
// dhaojdhoahodiihaoidhoiahdoiuuahywd

async function fetchCourseData() {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/courses/${courseId}`, {
      headers: {
        "Authentication-Token": store.state.user.token,
      },
    });

    const contentString = response.data.data.course.content;
    
    // Convert the JSON string back to an object
    const coursecontent = transformCourseData(JSON.parse(contentString));
    
    // Assign the transformed content (keeping it as an object)
    courseContent.value = coursecontent;
    
    is_data_fetched.value = true;

    // Ensure courseContent is not empty before accessing properties
    if (courseContent.value.length > 0 && courseContent.value[0].lectures.length > 0) {
      selectedContent.value = {
        type: "video",
        id: courseContent.value[0].lectures[0].id,
        data: courseContent.value[0].lectures[0],
      };
    }

  } catch (error) {
    console.error("Error fetching course data:", error);
  }
}


// dapijdiajdoijapoidjpioajdpoijapoidiuja

const currentWeek = computed(() => {
  if(is_data_fetched){
    return courseContent.value.find(week => {
    if (selectedContent.value.type === 'video') {
      return week.lectures.some(lecture => lecture.id === selectedContent.value.id);
    } else if (selectedContent.value.type === 'graded') {
      return week.gradedAssignments.some(assignment => assignment.id === selectedContent.value.id);
    } else {
      return week.practiceAssignments.some(assignment => assignment.id === selectedContent.value.id);
    }
  })?.week;
  }
});

function selectContent(type, content) {
  selectedContent.value = {
    type: type,
    id: content.id,
    data: content
  };
}

// these are used for submissions -----------------------------------------------------------------------------

async function fetchAssignmentSubmission(finalData) {
  try {
    const response = await axios.post(`http://127.0.0.1:5000/submissions`, finalData, {
      headers: {
        "Authentication-Token": store.state.user.token,
      },
    });
    console.log("Submission successful", response.data);
  } catch (error) {
    console.error("Error submitting assignment:", error);
  }
}


function storeSelectedAnswers() {
  const assignment = selectedContent.value.data;
  let data = "";

  const storedAnswers = assignment.questions.map((question, index) => ({
    id: index + 1, // Ensure ID is included
    option: [question.options[question.selectedAnswer]]
  }));
  
  if(contentType.value === "graded"){
    data = storedAnswers;
  }else{
    data = JSON.stringify(storedAnswers);
  }
  
  return data;
}

function submitAssignment() {
  const assignment = selectedContent.value.data;
  console.log(selectedContent.value.type)
  contentType.value = selectedContent.value.type
  console.log(expandedWeeks.value)
  let correctAnswers = 0;
  let totalQuestions = assignment.questions.length;

  assignment.questions.forEach(question => {
    if (question.selectedAnswer === question.correctAnswer) {
      correctAnswers++;
    }
  });

  const storedData = storeSelectedAnswers();
  console.log(storeSelectedAnswers());

  const submissionPayload = {
    assignment_id: `${courseId}-${expandedWeeks.value}-${selectedContent.value.id}`,
    content: storedData // Store content as expected JSON format
  };

  console.log(submissionPayload);
  
  alert(`You got ${correctAnswers} out of ${totalQuestions} questions correct!`);
  
  fetchAssignmentSubmission(submissionPayload); // Call API function with formatted JSON data
}

onBeforeMount(fetchCourseData);
</script>



<template>

  <div v-if="is_data_fetched" class="min-h-screen bg-gray-50 dark:bg-gray-900">
    <div class="flex h-screen">

      <!-- Sidebar -->
      <Transition name="slide">
        <div v-show="isSidebarOpen" class="w-80 bg-white dark:bg-gray-800 shadow-lg fixed md:relative h-screen z-40">

          <div class="h-full overflow-y-auto custom-scrollbar">
            <div class="p-4 pt-16 md:pt-4">
              <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Course Content</h2>
              <div class="h-px bg-gray-200 dark:bg-gray-700 mb-4"></div>

              <TransitionGroup name="list">
                <div v-for="week in courseContent" :key="week.week" class="mb-4">
                  <Disclosure v-slot="{ open }" :defaultOpen="expandedWeeks.includes(week.week)">
                    <DisclosureButton as="button" @click="updateExpandedWeeks(week.week)"
                      class="flex items-center w-full p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-200">
                      <ChevronDown v-if="open"
                        class="h-5 w-5 mr-2 text-gray-500 dark:text-gray-400 transform transition-transform duration-200" />
                      <ChevronRight v-else
                        class="h-5 w-5 mr-2 text-gray-500 dark:text-gray-400 transform transition-transform duration-200" />
                      <div>
                        <div class="font-medium text-left text-gray-900 dark:text-white">Week {{ week.week }}</div>
                        <div class="text-sm text-gray-500 dark:text-gray-400 text-left">{{ week.title }}</div>
                      </div>
                    </DisclosureButton>

                    <Transition name="collapse">
                      <div v-show="open" class="pl-7 mt-2 space-y-2 overflow-hidden">
                        <!-- Lectures -->
                        <div class="mb-2">
                          <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Lectures</div>
                          <button v-for="lecture in week.lectures" :key="lecture.id"
                            @click="selectContent('video', lecture)" :class="[
                              'flex items-center w-full p-2 rounded-md text-left text-sm transition-all duration-200',
                              'hover:bg-gray-100 dark:hover:bg-gray-700 transform hover:translate-x-1',
                              selectedContent.type === 'video' && selectedContent.id === lecture.id ? 'bg-gray-100 dark:bg-gray-700 translate-x-1' : ''
                            ]">
                            <Play class="h-4 w-4 mr-2 text-gray-500 dark:text-gray-400" />
                            <span class="text-gray-700 dark:text-gray-300">{{ lecture.title }}</span>
                          </button>
                        </div>

                        <!-- Graded Assignments -->
                        <div class="mb-2">
                          <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Graded Assignments
                          </div>
                          <button v-for="assignment in week.gradedAssignments" :key="assignment.id"
                            @click="selectContent('graded', assignment)" :class="[
                              'flex items-center w-full p-2 rounded-md text-left text-sm transition-all duration-200',
                              'hover:bg-gray-100 dark:hover:bg-gray-700 transform hover:translate-x-1',
                              selectedContent.type === 'graded' && selectedContent.id === assignment.id ? 'bg-gray-100 dark:bg-gray-700 translate-x-1' : ''
                            ]">
                            <ClipboardCheck class="h-4 w-4 mr-2 text-emerald-500" />
                            <span class="text-gray-700 dark:text-gray-300">{{ assignment.title }}</span>
                          </button>
                        </div>

                        <!-- Practice Assignments -->
                        <div>
                          <div class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Practice</div>
                          <button v-for="practice in week.practiceAssignments" :key="practice.id"
                            @click="selectContent('practice', practice)" :class="[
                              'flex items-center w-full p-2 rounded-md text-left text-sm transition-all duration-200',
                              'hover:bg-gray-100 dark:hover:bg-gray-700 transform hover:translate-x-1',
                              selectedContent.type === 'practice' && selectedContent.id === practice.id ? 'bg-gray-100 dark:bg-gray-700 translate-x-1' : ''
                            ]">
                            <Pencil class="h-4 w-4 mr-2 text-blue-500" />
                            <span class="text-gray-700 dark:text-gray-300">{{ practice.title }}</span>
                          </button>
                        </div>
                      </div>
                    </Transition>
                  </Disclosure>
                </div>
              </TransitionGroup>
            </div>
          </div>
        </div>
      </Transition>

      <!-- Main content area -->
      <div :class="[
        'flex-1 p-4 transition-all duration-300 ease-in-out',
        isSidebarOpen ? 'md:ml-0' : 'ml-0'
      ]">
        <div class="max-w-4xl mx-auto pt-16 md:pt-4">
          <h1 class="text-3xl font-bold mb-6 text-gray-900 dark:text-white">Programming Fundamentals</h1>

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
            <Transition name="fade" mode="out-in">
              <!-- Video Content -->
              <div v-if="selectedContent.type === 'video'" :key="'video'">
                <div class="aspect-video bg-black rounded-md overflow-hidden">
                  <iframe :key="selectedContent.data.videoId" class="w-full h-full"
                    :src="'https://www.youtube.com/embed/' + selectedContent.data.videoId" title="Course Video"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen></iframe>
                </div>
                <div class="mt-4">
                  <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                    {{ selectedContent.data.title }}
                  </h3>
                  <div class="flex items-center text-sm text-gray-500 dark:text-gray-400 mt-2">
                    <BookOpen class="h-4 w-4 mr-2" />
                    <span>Week {{ currentWeek }}</span>
                  </div>
                </div>
              </div>

              <!-- Assignment Content -->
              <div v-else :key="'assignment'" class="space-y-6">
                <div class="flex items-center justify-between">
                  <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                    {{ selectedContent.data.title }}
                  </h3>
                  <span :class="[
                    'px-3 py-1 rounded-full text-sm font-medium',
                    selectedContent.type === 'graded'
                      ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-100'
                      : 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-100'
                  ]">
                    {{ selectedContent.type === 'graded' ? 'Graded' : 'Practice' }}
                  </span>
                </div>

                <div v-for="(question, index) in selectedContent.data.questions" :key="index"
                  class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p class="text-gray-900 dark:text-white font-medium mb-4">{{ index + 1 }}. {{ question.text }}</p>
                  <div class="space-y-2">
                    <label v-for="(option, optIndex) in question.options" :key="optIndex" :class="[
                      'flex items-center p-3 rounded-lg cursor-pointer transition-all duration-200',
                      question.selectedAnswer === optIndex
                        ? 'bg-blue-100 dark:bg-blue-900 border-2 border-blue-500'
                        : 'bg-white dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-600 border-2 border-transparent'
                    ]">
                      <input type="radio" :name="'question-' + index" :value="optIndex"
                        v-model="question.selectedAnswer" class="hidden" />
                      <span class="text-gray-700 dark:text-gray-300">{{ option }}</span>
                    </label>
                  </div>
                </div>

                <button @click="submitAssignment"
                  class="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors duration-200">
                  Submit Assignment
                </button>
              </div>
            </Transition>
            <Aibot></Aibot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background-color: rgba(156, 163, 175, 0.7);
}

/* Slide transition for sidebar */
.slide-enter-active,
.slide-leave-active {
  transition: transform 0.3s ease-in-out;
}

.slide-enter-from,
.slide-leave-to {
  transform: translateX(-100%);
}

/* Fade transition for content */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* List transitions */
.list-move,
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Lectures transitions */
.lectures-move,
.lectures-enter-active,
.lectures-leave-active {
  transition: all 0.3s ease;
}

.lectures-enter-from,
.lectures-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.collapse-enter-active,
.collapse-leave-active {
  transition: max-height 0.3s ease-in-out, opacity 0.3s ease-in-out;
  max-height: 1000px;
}

.collapse-enter-from,
.collapse-leave-to {
  max-height: 0;
  opacity: 0;
}

@media (prefers-color-scheme: dark) {
  .custom-scrollbar {
    scrollbar-color: rgba(75, 85, 99, 0.5) transparent;
  }

  .custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: rgba(75, 85, 99, 0.5);
  }

  .custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background-color: rgba(75, 85, 99, 0.7);
  }
}
</style>





<!-- 
// const courseContent = [
//     {
//       "week": 1,
//       "title": "Introduction to Programming",
//       "lectures": [
//         { "id": 1, "title": "Getting Started", "videoId": "W6NZfCO5SIk" },
//         { "id": 2, "title": "Basic Concepts", "videoId": "PkZNo7MFNFg" }
//       ],
//       "gradedAssignments": [
//         {
//           "id": 101,
//           "title": "Programming Basics Quiz",
//           "questions": [
//             {
//               "text": "What is a variable?",
//               "options": [
//                 "A container for storing data values",
//                 "A mathematical operation",
//                 "A type of loop",
//                 "A function name"
//               ],
//               "correctAnswer": 0
//             },
//             {
//               "text": "Which of the following is a valid variable name in JavaScript?",
//               "options": [
//                 "123variable",
//                 "_myVariable",
//                 "my-variable",
//                 "class"
//               ],
//               "correctAnswer": 1
//             }
//           ]
//         }
//       ],
//       "practiceAssignments": [
//         {
//           "id": 201,
//           "title": "Variables Practice",
//           "questions": [
//             {
//               "text": "What will be the output of: console.log(typeof 42)?",
//               "options": [
//                 "string",
//                 "number",
//                 "integer",
//                 "float"
//               ],
//               "correctAnswer": 1
//             }
//           ]
//         }
//       ]
//     },
//     {
//       "week": 2,
//       "title": "Control Structures",
//       "lectures": [
//         { "id": 3, "title": "Conditional Statements", "videoId": "7WiJGTPuVeU" },
//         { "id": 4, "title": "Loops and Iterations", "videoId": "s9wW2PpJsmQ" }
//       ],
//       "gradedAssignments": [
//         {
//           "id": 102,
//           "title": "Control Flow Assessment",
//           "questions": [
//             {
//               "text": "Which statement is used to exit a loop in JavaScript?",
//               "options": [
//                 "exit",
//                 "break",
//                 "return",
//                 "continue"
//               ],
//               "correctAnswer": 1
//             }
//           ]
//         }
//       ],
//       "practiceAssignments": [
//         {
//           "id": 202,
//           "title": "Loops Practice",
//           "questions": [
//             {
//               "text": "What is the output of: for(let i=0; i<3; i++) { console.log(i); }",
//               "options": [
//                 "0, 1, 2",
//                 "1, 2, 3",
//                 "0, 1, 2, 3",
//                 "1, 2"
//               ],
//               "correctAnswer": 0
//             }
//           ]
//         }
//       ]
//     },
//     {
//       "week": 3,
//       "title": "Functions and Objects",
//       "lectures": [
//         { "id": 5, "title": "Functions Basics", "videoId": "N8ap4k_1QEQ" },
//         { "id": 6, "title": "Object-Oriented Programming", "videoId": "PFmuCDHHpwk" }
//       ],
//       "gradedAssignments": [
//         {
//           "id": 103,
//           "title": "Functions Quiz",
//           "questions": [
//             {
//               "text": "What is a pure function?",
//               "options": [
//                 "A function that only uses global variables",
//                 "A function that always returns the same output for the same input",
//                 "A function that modifies its parameters",
//                 "A function without parameters"
//               ],
//               "correctAnswer": 1
//             }
//           ]
//         }
//       ],
//       "practiceAssignments": [
//         {
//           "id": 203,
//           "title": "Objects Practice",
//           "questions": [
//             {
//               "text": "How do you access a property named 'age' in an object 'person'?",
//               "options": [
//                 "person[age]",
//                 "person->age",
//                 "person.age",
//                 "person::age"
//               ],
//               "correctAnswer": 2
//             }
//           ]
//         }
//       ]
//     }
//   ] -->
