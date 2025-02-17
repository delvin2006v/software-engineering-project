<script setup>
import { ref, computed } from 'vue'
import { Disclosure, DisclosureButton } from '@headlessui/vue'
import { ChevronDown, ChevronRight, Play, BookOpen, Menu, X } from 'lucide-vue-next'

const courseContent = [
  {
    week: 1,
    title: "Introduction to Programming",
    lectures: [
      { id: 1, title: "Getting Started", videoId: "W6NZfCO5SIk" },
      { id: 2, title: "Basic Concepts", videoId: "PkZNo7MFNFg" },
    ]
  },
  {
    week: 2,
    title: "Control Structures",
    lectures: [
      { id: 3, title: "Conditional Statements", videoId: "7WiJGTPuVeU" },
      { id: 4, title: "Loops and Iterations", videoId: "s9wW2PpJsmQ" },
    ]
  },
  {
    week: 3,
    title: "Functions and Objects",
    lectures: [
      { id: 5, title: "Functions Basics", videoId: "N8ap4k_1QEQ" },
      { id: 6, title: "Object-Oriented Programming", videoId: "PFmuCDHHpwk" },
    ]
  },
]

const selectedVideo = ref(courseContent[0].lectures[0].videoId)
const expandedWeeks = ref([1])
const isSidebarOpen = ref(true)

const currentLecture = computed(() => {
  return courseContent
    .flatMap(week => week.lectures)
    .find(lecture => lecture.videoId === selectedVideo.value)
})

const currentWeek = computed(() => {
  return courseContent.find(week => 
    week.lectures.some(lecture => lecture.videoId === selectedVideo.value)
  )?.week
})
</script>


<template>
    <div class="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div class="flex h-screen">
        <!-- Sidebar Toggle Button -->
        <!-- <button 
          @click="isSidebarOpen = !isSidebarOpen"
          class="fixed top-4 left-4 z-50 p-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        >
          <Menu v-if="!isSidebarOpen" class="h-5 w-5 text-gray-600 dark:text-gray-300" />
          <X v-else class="h-5 w-5 text-gray-600 dark:text-gray-300" />
        </button> -->
  
        <!-- Sidebar -->
        <Transition name="slide">
          <div 
            v-show="isSidebarOpen"
            class="w-80 bg-white dark:bg-gray-800 shadow-lg fixed md:relative h-screen z-40"
          >
            <div class="h-full overflow-y-auto custom-scrollbar">
              <div class="p-4 pt-16 md:pt-4">
                <h2 class="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Course Content</h2>
                <div class="h-px bg-gray-200 dark:bg-gray-700 mb-4"></div>
                
                <TransitionGroup name="list">
                  <div v-for="week in courseContent" :key="week.week" class="mb-4">
                    <Disclosure v-slot="{ open }" :defaultOpen="expandedWeeks.includes(week.week)">
                      <DisclosureButton 
                        class="flex items-center w-full p-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-700 transition-all duration-200"
                      >
                        <ChevronDown
                          v-if="open"
                          class="h-5 w-5 mr-2 text-gray-500 dark:text-gray-400 transform transition-transform duration-200"
                        />
                        <ChevronRight
                          v-else
                          class="h-5 w-5 mr-2 text-gray-500 dark:text-gray-400 transform transition-transform duration-200"
                        />
                        <div>
                          <div class="font-medium text-left text-gray-900 dark:text-white">Week {{ week.week }}</div>
                          <div class="text-sm text-gray-500 dark:text-gray-400 text-left">{{ week.title }}</div>
                        </div>
                      </DisclosureButton>
  
                      <Transition name="collapse">
                          <div v-show="open" class="pl-7 mt-2 space-y-2 overflow-hidden">
                            <button
                              v-for="lecture in week.lectures"
                              :key="lecture.id"
                              @click="selectedVideo = lecture.videoId"
                              :class="[
                                'flex items-center w-full p-2 rounded-md text-left text-sm transition-all duration-200',
                                'hover:bg-gray-100 dark:hover:bg-gray-700 transform hover:translate-x-1',
                                selectedVideo === lecture.videoId ? 'bg-gray-100 dark:bg-gray-700 translate-x-1' : ''
                              ]"
                            >
                              <Play class="h-4 w-4 mr-2 text-gray-500 dark:text-gray-400" />
                              <span class="text-gray-700 dark:text-gray-300">{{ lecture.title }}</span>
                            </button>
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
        <div 
          :class="[ 
            'flex-1 p-4 transition-all duration-300 ease-in-out',
            isSidebarOpen ? 'md:ml-0' : 'ml-0'
          ]"
        >
          <div class="max-w-4xl mx-auto pt-16 md:pt-4">
            <h1 class="text-3xl font-bold mb-6 text-gray-900 dark:text-white">Programming Fundamentals</h1>
            
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4">
              <Transition name="fade" mode="out-in">
                <div class="aspect-video bg-black rounded-md overflow-hidden">
                  <iframe
                    :key="selectedVideo"
                    class="w-full h-full"
                    :src="'https://www.youtube.com/embed/' + selectedVideo"
                    title="Course Video"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                  ></iframe>
                </div>
              </Transition>
              
              <Transition name="fade" mode="out-in">
                <div :key="selectedVideo" class="mt-4">
                  <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                    {{ currentLecture?.title }}
                  </h3>
                  <div class="flex items-center text-sm text-gray-500 dark:text-gray-400 mt-2">
                    <BookOpen class="h-4 w-4 mr-2" />
                    <span>Week {{ currentWeek }}</span>
                  </div>
                </div>
              </Transition>
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

  .lectures-enter-active, .lectures-leave-active {
  transition: max-height 0.3s ease-in-out, opacity 0.3s ease-in-out;
}

.lectures-enter-from, .lectures-leave-to {
  max-height: 0;
  opacity: 0;
}

.lectures-enter-to, .lectures-leave-from {
  max-height: 500px; /* Adjust based on content size */
  opacity: 1;
}
  </style>
  