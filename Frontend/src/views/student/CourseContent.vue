<script setup>
import { ref, computed, onMounted, onBeforeMount } from 'vue';
import { Disclosure, DisclosureButton } from '@headlessui/vue';
import { ChevronDown, ChevronRight, Play, BookOpen, ClipboardCheck, Pencil, Menu, SquareCode, PlayCircleIcon, CheckCircle2Icon, XCircleIcon } from 'lucide-vue-next';
import Aibot from './Aibot.vue';
import { toast, Toaster } from 'vue-sonner'
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
const code_store = ref({})
const code_fetched = ref({})

let expandedWeeks = ref([1]);
const assignment = ref({});

// this is for expanded week chnages
function updateExpandedWeeks(newWeek) {
  expandedWeeks.value = [newWeek];
}


async function fetchCourseData() {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/courses/${courseId}`, {
      headers: {
        "Authentication-Token": store.state.user.token,
      },
    });

    const contentString = response.data.data.course.content;
    
    // Convert the JSON string back to an object
    const coursecontent = JSON.parse(contentString);
    
    // Assign the transformed content (keeping it as an object)
    courseContent.value = coursecontent;
    
    is_data_fetched.value = true;

    // Ensure courseContent is not empty before accessing properties
    if (courseContent.value.length > 0 && courseContent.value[0].items.length > 0) {
      selectContent(courseContent.value[0].items[0])
    }

  } catch (error) {
    console.error("Error fetching course data:", error);
  }
}

function selectContent(item) {

  if (item.type == 'practice-assignment' || item.type == 'graded-assignment') {
    for (const question of item.questions) {
      if (question.type == 'option-many') {
        question.selectedAnswer = []
      }
    } 
  }
  selectedContent.value = item;
  if (item.type == 'practice-assignment' || item.type == 'graded-assignment') {
    fetchAssignmentSubmission()
  }
  if (item.type == 'programming-assignment'){
    fetchAssignmentSubmission()
    console.log(selectedContent.value)
    assignment.value = selectedContent.value
  }
}


// this is for programming assignment test 


const code = ref('')
const result = ref(null)

const runCode = async () => {
  if (!code.value.trim()) {
    toast.error('Please enter some code before submitting')
    return
  }

  try {
    code_store.value = code.value
    console.log(code_store.value)
    // Simulate code execution (in a real app, this would call your backend)
    const submissionPayload = {
      assignment_id: `${courseId}-${expandedWeeks.value}-${selectedContent.value.id}`,
      content: code_store.value, // Store content as expected JSON format
    };

    MakeAssignmentSubmission(submissionPayload);

  } catch (error) {
    console.log('Failed to execute code')
  }
}

// these are used for submissions -----------------------------------------------------------------------------
function is_selected(question, option) {
  if (question.type == 'option-many') {
    return question.selectedAnswer.includes(option)
  } else {
    return question.selectedAnswer === option
  }
}

function updateEval(result) {
  selectedContent.value.eval = "yes";
  const len = selectedContent.value.questions.length
  console.log(selectedContent.value.questions)
  for (let i=0; i< len; i++) {
    if (selectedContent.value.questions[i].type == 'option-many') {
      selectedContent.value.questions[i].selectedAnswer = result.content[i].option
    }else {
      selectedContent.value.questions[i].selectedAnswer = result.content[i].option[0]
    }
    if (result.content[i].correct == 1) {
      selectedContent.value.questions[i].correct = 1;
    }
  }
}

async function MakeAssignmentSubmission(finalData) {
  console.log(finalData)
  try {
    const response = await axios.post(`http://127.0.0.1:5000/submissions`, finalData, {
      headers: {
        "Authentication-Token": store.state.user.token,
      },
    });
    console.log("Submission successful", response.data);
    let result = response.data.data;

    if (selectedContent.value.type != "programming-assignment"){
        updateEval(result)
    }
    fetchAssignmentSubmission()

  } catch (error) {
    console.error("Error submitting assignment:", error);
  }
}

async function fetchAssignmentSubmission() {
   try {
    let assignment_id = courseId + '-' + expandedWeeks.value + '-' + selectedContent.value.id
    const response = await axios.get(`http://127.0.0.1:5000/submissions/` + assignment_id, {
      headers: {
        "Authentication-Token": store.state.user.token,
      },
    });
    let output_result = JSON.parse(response.data.data.submission.content);
    if (response.data.status.success == 1) {
      if (selectedContent.value.type != "programming-assignment"){
      updateEval({'content': output_result})
      }else{
        const output = output_result.cases[0].output
        const passed = output_result.cases[0].pass === 1 ? true : false;
        code.value = output_result.code
        result.value = { passed , output }
      }
    }

  } catch (error) {
    console.error("Error submitting assignment:", error);
  }

}

function prepareOutput(question) {
  if (question.type == 'option-many') {
    return {
      id: question.id,
      option: question.selectedAnswer
    }
  } else {
    return {
      id: question.id,
      option: [question.selectedAnswer]
    }
  }
}

function storeSelectedAnswers() {
  const assignment = selectedContent.value;
  let data = "";

  const storedAnswers = assignment.questions.map(prepareOutput);
  
  console.log(storedAnswers)

  data = JSON.stringify(storedAnswers);
  
  return data;
}

function submitAssignment() {
    const assignment = selectedContent.value;
    console.log("this is it", selectedContent.value.type);
    contentType.value = selectedContent.value.type;
    console.log(expandedWeeks.value);
    // let correctAnswers = 0;
    // let totalQuestions = assignment.questions.length;
    const storedData = storeSelectedAnswers();

    const submissionPayload = {
      assignment_id: `${courseId}-${expandedWeeks.value}-${selectedContent.value.id}`,
      content: storedData, // Store content as expected JSON format
    };

    // console.log(submissionPayload);
    MakeAssignmentSubmission(submissionPayload); // Call API function with formatted JSON data
  }

onBeforeMount(fetchCourseData);
</script>



<template>

  <div v-if="is_data_fetched" class="min-h-full bg-gray-50 dark:bg-gray-900">
    <div class="flex h-screen">

      <!-- Sidebar -->
      <Transition name="slide">
        <div v-show="isSidebarOpen" class="w-80 bg-white dark:bg-gray-800 shadow-lg fixed md:relative min-h-full z-40">

          <div class="min-h-screen overflow-y-auto custom-scrollbar">
            <div class="p-4 pt-16 md:pt-4">
              <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Course Content</h2>
              <div class="h-px bg-gray-200 dark:bg-gray-700 mb-4"></div>

              <TransitionGroup name="list">
                <div v-for="section in courseContent" :key="section.id" class="mb-4">
                  <Disclosure v-slot="{ open }" :defaultOpen="expandedWeeks.includes(section.id)">
                    <DisclosureButton as="button" @click="updateExpandedWeeks(section.id)"
                      class="flex items-center w-full p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-200">
                      <ChevronDown v-if="open"
                        class="h-5 w-5 mr-2 text-gray-500 dark:text-gray-400 transform transition-transform duration-200" />
                      <ChevronRight v-else
                        class="h-5 w-5 mr-2 text-gray-500 dark:text-gray-400 transform transition-transform duration-200" />
                      <div>
                        <div class="font-medium text-left text-gray-900 dark:text-white">{{ section.title }}</div>
                      </div>
                    </DisclosureButton>

                    <Transition name="collapse">
                      <div v-show="open" class="pl-7 mt-2 space-y-2 overflow-hidden">
                        <!-- Lectures -->
                        <div class="mb-2">
                          <button v-for="item in section.items" :key="item.id"
                            @click="selectContent(item)" :class="[
                              'flex items-center w-full p-2 ps-1 rounded-md text-left text-sm transition-all duration-200',
                              'hover:bg-gray-100 dark:hover:bg-gray-700 transform hover:translate-x-1',
                              selectedContent.type === item.type && selectedContent.id === item.id ? 'bg-gray-100 dark:bg-gray-700 translate-x-1' : ''
                            ]">
                            <Play v-if="item.type == 'lecture'" class="h-4 w-4 mr-2 text-gray-500 dark:text-gray-400" />
                            <ClipboardCheck v-if="item.type == 'graded-assignment'" class="h-4 w-4 mr-2 text-emerald-500" />
                            <Pencil v-if="item.type == 'practice-assignment'" class="h-4 w-4 mr-2 text-blue-500" />
                            <SquareCode v-if="item.type == 'programming-assignment'" class="h-4 w-4 mr-2 text-red-500" />

                            <span class="text-gray-700 dark:text-gray-300">{{ item.title }}</span>
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

          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
            <Transition name="fade" mode="out-in">
              <!-- Video Content -->
              <div v-if="selectedContent.type === 'lecture'" :key="selectedContent.id">
                <div class="my-4">
                  <h3 class="text-2xl font-semibold text-gray-900 dark:text-white">
                    {{ selectedContent.title }}
                  </h3>
                </div>
                <div class="aspect-video bg-black rounded-md overflow-hidden">
                  <iframe :key="selectedContent.url" class="w-full h-full"
                    :src="'https://www.youtube.com/embed/' + selectedContent.url" title="Course Video"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen></iframe>
                </div>
              </div>

              <!-- Programming Assignment -->
              <div v-else-if="selectedContent.type == 'programming-assignment'" :key="selectedContent.id">

                <div class="flex items-center justify-between">
                  <!-- this is for programming assignment  -->
                  <div class="min-h-screen bg-background py-8 px-4 scroll-container">
                    <div class="max-w-4xl mx-auto space-y-8">
                      <!-- Assignment Details -->
                      <div class="bg-card text-card-foreground rounded-lg shadow-md overflow-hidden">
                        <div class="p-6">
                          <h2 class="text-2xl font-bold">{{ assignment.title }}</h2>
                          <p class="text-lg mt-2 text-muted-foreground">
                            Type: {{ assignment.type }}
                          </p>
                        </div>
                        <div class="px-6 pb-6">
                          <div class="prose dark:prose-invert max-w-none">
                            <h3 class="text-lg font-semibold mb-2">Question:</h3>
                            <p class="text-card-foreground">{{ assignment.question }}</p>
                          </div>
                        </div>
                      </div>

                      <!-- Code Editor -->
                      <div class="bg-card text-card-foreground rounded-lg shadow-md overflow-hidden">
                        <div class="p-6">
                          <div class="flex items-center gap-2 mb-4">
                            <play-circle-icon class="w-5 h-5" />
                            <h2 class="text-xl font-semibold">Python Code Editor</h2>
                          </div>
                          <textarea
                            v-model="code"
                            placeholder="Enter your Python code here..."
                            class="w-full min-h-[200px] p-4 font-mono bg-muted text-foreground rounded-md border border-input focus:outline-none focus:ring-2 focus:ring-ring"
                          />
                          <button
                            @click="runCode"
                            class="mt-4 w-full bg-primary text-primary-foreground hover:bg-primary/90 py-3 px-6 rounded-md font-medium transition-colors"
                          >
                            Run Code
                          </button>
                        </div>
                      </div>

                      <!-- Results -->
                      <div v-if="result" class="bg-card text-card-foreground rounded-lg shadow-md overflow-hidden">
                        <div class="p-6">
                          <div class="flex items-center gap-2 mb-4">
                            <check-circle-2-icon v-if="result.passed" class="w-5 h-5 text-green-500" />
                            <x-circle-icon v-else class="w-5 h-5 text-red-500" />
                            <h2 class="text-xl font-semibold">Test Results</h2>
                          </div>
                          <div class="bg-muted p-4 rounded-lg">
                            <h4 class="font-semibold mb-2">Output:</h4>
                            <pre class="whitespace-pre-wrap font-mono text-sm">{{ result.output }}</pre>
                          </div>
                          <div
                            :class="[
                              'mt-4 p-4 rounded-lg',
                              result.passed
                                ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300'
                                : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300'
                            ]"
                          >
                            {{ result.passed ? '✅ All test cases passed!' : '❌ Some test cases failed. Please check your code and try again.' }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <Toaster position="top-right" />
                </div>
              </div>

              <!-- Assignment Content -->
              <div v-else :key="selectedContent.id" class="min-h-screen space-y-6 scroll-container_2">
                <div class="flex items-center justify-between">
                  <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                    {{ selectedContent.title }}
                  </h3>
                  <span :class="[
                    'px-3 py-1 rounded-full text-sm font-medium',
                    selectedContent.type === 'graded-assignment'
                      ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900 dark:text-emerald-100'
                      : 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-100'
                  ]">
                    {{ selectedContent.type === 'graded-assignment' ? 'Graded' : 'Practice' }}
                  </span>
                </div>

                <div v-for="question in selectedContent.questions" :key="question.id"
                  class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p class="text-gray-900 dark:text-white font-medium mb-4">{{ question.id }}. {{ question.question }}</p>
                  <div class="space-y-2">
                    <label v-for="(option, optIndex) in question.options" :key="optIndex" :class="[
                      'flex items-center p-3 rounded-lg cursor-pointer transition-all duration-200',
                      is_selected(question, option)
                        ? 'bg-blue-100 dark:bg-blue-900 border-2 border-blue-500'
                        : 'bg-white dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-600 border-2 border-transparent'
                    ]">
                      <input v-if="question.type == 'option-one'" type="radio" :name="'question-' + question.id" :value="option"
                        v-model="question.selectedAnswer" class='hidden'/>
                      <input v-if="question.type == 'option-many'" type="checkbox" :id="'question-' + question.id + '-' + optIndex" :value="option"
                        v-model="question.selectedAnswer" class='hidden'/>
                      <span class="text-gray-700 dark:text-gray-300">{{ option }}</span>
                    </label>
                    <input v-if="question.type == 'text'" type="text" :name="'question-' + question.id" v-model="question.selectedAnswer"
                    class="block w-full rounded-md border-gray-300 px-3 py-2 text-white-900 shadow-sm focus:ring-2 focus:ring-blue-600 focus:outline-none sm:text-sm transition-all duration-300  dark:bg-gray-800 border-2 border-transparent"
                    >
                    <div class="space-y-2">
                        <label v-if="selectedContent.eval == 'yes'"
                          :class="[question.correct ? 'text-green-500' : 'text-red-500']"
                        >
                          {{ question.correct == 1 ? 'Your answer is correct' : 'Your answer is wrong ' }}<br><br v-if="question.correct != 1">
                          <label v-if="question.correct != 1">Correct Answer(s) :</label><br>
                          <div>
                              <label v-for="answer in question.answer">
                                {{answer}}<br>
                              </label>
                          </div>
                        </label>
                    </div>
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

/* Scrollable container */
.scroll-container {
  max-height: 500px; /* Set a max height */
  overflow-y: auto; /* Enable vertical scrolling */
  padding-right: 8px; /* Avoid cutting off content */
  margin-left: 90px;
}

.scroll-container_2 {
  max-height: 500px; /* Set a max height */
  overflow-y: auto; /* Enable vertical scrolling */
  padding-right: 8px; /* Avoid cutting off content */
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