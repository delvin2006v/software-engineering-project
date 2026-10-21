<script setup>
import { ref, computed,onBeforeMount } from 'vue'
import { Trash2, Upload, FileText, Clock, Search } from 'lucide-vue-next'
import axios from 'axios'
import {useStore} from 'vuex'
import { useRoute } from 'vue-router'

const title = ref('')
const materialType = ref('pdf')
const selectedFile = ref(null)
const uploads = ref([])
const searchQuery = ref('')
const store = useStore()
const route = useRoute()
const successfullyUploaded = ref(false)
const courseId =route.params.id 
const handleFileChange = (event) => {
  selectedFile.value = event.target.files[0]
}

//Get Previous Material
async function previousCourses(){

  const response = await axios.get(`http://127.0.0.1:5000/courses/${courseId}/materials`,{
      headers: {
          'Authentication-Token': store.state.user.token,
        }}
        )
      const nextupload =  ref([])
      for (const material of response.data.data.materials) {
        let newupload = {
            id:material.id ,
            title: material.title,
            type: material.type,
            fileName: material.path,
          }
        
        nextupload.value.unshift(newupload)

      }
      uploads.value = nextupload.value
         
      
}
// Delete upload
async function deleteOneUpload(materialId){
try{
  const response = await axios.delete(`http://127.0.0.1:5000/courses/${courseId}/materials/${materialId}`,{
      headers: {
          'Authentication-Token': store.state.user.token,
        }}
        )
      
}catch(error){
 console.log(error.message)
} 
      
}

const handleSubmit = () => {
  if (!title.value || !selectedFile.value) return

   const newupload= {
    title: title.value,
    type: materialType.value,
    fileName: selectedFile.value.name,
    
  }

  // Create FormData object
  const formData = new FormData();
  formData.append('title', title.value);
  formData.append('type', materialType.value);
  formData.append('file', selectedFile.value);
  
  axios.post(`http://127.0.0.1:5000/courses/${courseId}/materials`,formData,{
    headers: {
        'Content-Type': 'multipart/form-data',
        'Authentication-Token': store.state.user.token,
      },
  }).then(function (response) {
    console.log(response);
    successfullyUploaded.value = true
    previousCourses()
    setTimeout(() => { 
     successfullyUploaded.value = false
    }, 3000);

  })
  .catch(function (error) {
    console.log(error);
  });

  // Reset form
  title.value = ''
  materialType.value = 'pdf'
  selectedFile.value = null
  
  // Reset file input
  document.getElementById('file-upload').value = ''
}



const deleteUpload = (id) => {
  const index = uploads.value.findIndex(upload => upload.id === id)
  if (index !== -1) {
    const element = document.querySelector(`[data-id="${id}"]`)
    element.classList.add('animate-slide-out')
    setTimeout(() => {
      uploads.value = uploads.value.filter(upload => upload.id !== id)
    }, 300)
  }
  console.log('DeleteUpload ssssss',id)
  deleteOneUpload(id)
}

const filteredUploads = computed(() => {
  const query = searchQuery.value.toLowerCase()
  return uploads.value.filter(upload => 
    upload.title.toLowerCase().includes(query) ||
    upload.fileName.toLowerCase().includes(query) ||
    upload.type.toLowerCase().includes(query)
  )
})

const stats = {
  totalUploads: computed(() => uploads.value.length),
  pdfCount: computed(() => uploads.value.filter(u => u.type === 'pdf').length),
  textCount: computed(() => uploads.value.filter(u => u.type === 'text').length),
  otherCount: computed(() => uploads.value.filter(u => u.type === 'other').length)
}

onBeforeMount(previousCourses)
</script>

<template>
  <div class="min-h-screen p-8">
    <div class="container mx-auto">
      <h1 class="text-3xl font-bold mb-8 text-center">File Upload System</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8 text-center">
        <!-- Upload Form -->
        <div class="bg-card p-6 rounded-lg shadow-lg animate-slide-up hover:shadow-xl transition-all duration-300 border border-gray-600">
          <h2 class="text-xl font-semibold mb-6 flex items-center gap-2">
            <Upload class="w-5 h-5" />
            Upload New Material
          </h2>
          
          <form @submit.prevent="handleSubmit" class="space-y-4">
            <div class="group">
              <label class="block text-sm font-medium mb-2 group-hover:text-primary transition-colors">Title</label>
              <input
                v-model="title"
                type="text"
                class="w-full px-4 py-2 rounded-md bg-secondary text-foreground border border-border focus:outline-none focus:ring-2 focus:ring-primary transition-all hover:border-primary"
                required
              />
            </div>
            
            <div class="group">
              <label class="block text-sm font-medium mb-2 group-hover:text-primary transition-colors">Material Type</label>
              <select
                v-model="materialType"
                class="w-full px-4 py-2 rounded-md bg-secondary text-foreground border border-border focus:outline-none focus:ring-2 focus:ring-primary transition-all hover:border-primary"
              >
                <option value="pdf">PDF</option>
                <option value="text">Text File</option>
                <option value="other">Other</option>
              </select>
            </div>
            
            <div class="group">
              <label class="block text-sm font-medium mb-2 group-hover:text-primary transition-colors">File</label>
              <input
                id="file-upload"
                type="file"
                @change="handleFileChange"
                class="w-full px-4 py-2 rounded-md bg-secondary text-foreground border border-border focus:outline-none focus:ring-2 focus:ring-primary transition-all hover:border-primary"
                required
              />
            </div>
            
            <button
              type="submit"
              class="w-full bg-primary text-primary-foreground px-6 py-2 rounded-md hover:opacity-90 transition-all duration-300 transform hover:scale-[1.02] hover:shadow-lg flex items-center justify-center gap-2"
            >
              <Upload class="w-4 h-4" />
              Upload Material
            </button>
          </form><br>
          <span v-if="successfullyUploaded" class="m-2 font-bold text-center bg-white p-5 text-black" >Successfully uploaded</span>
        </div>
        
        <!-- Upload List -->
        <div class="bg-card p-6 rounded-lg shadow-lg animate-slide-up hover:shadow-xl transition-all duration-300 border border-gray-600">
          <div class="flex flex-col h-full">
            <h2 class="text-xl font-semibold mb-4 flex items-center gap-2">
              <FileText class="w-5 h-5" />
              Previous Uploads
            </h2>
            
            <!-- Search Bar -->
            <div class="relative mb-4 group">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search class="h-4 w-4 text-muted-foreground group-focus-within:text-primary transition-colors" />
              </div>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search uploads..."
                class="w-full pl-10 px-4 py-2 rounded-md bg-secondary text-foreground border border-border focus:outline-none focus:ring-2 focus:ring-primary transition-all hover:border-primary"
              />
            </div>
            
            <!-- Scrollable List with Custom Scrollbar -->
            <div class="flex-1 overflow-hidden">
              <div class="space-y-4 h-[400px] overflow-y-auto custom-scrollbar pr-2">
                <div
                  v-for="upload in filteredUploads"
                  :key="upload.id"
                  :data-id="upload.id"
                  class="bg-secondary p-4 rounded-md flex justify-between items-start group animate-slide-down hover:shadow-md transition-all duration-300 border border-gray-700"
                >
                  <div>
                    <h3 class="font-medium group-hover:text-primary transition-colors">{{ upload.title }}</h3>
                    <a :href="'http://localhost:5000' + upload.fileName" target="_blank" class="text-sm text-muted-foreground">{{ upload.fileName }}</a>
                    <div class="flex items-center gap-2 text-xs text-muted-foreground">
                      <Clock class="w-3 h-3" />
                      <span>{{ upload.date }}</span>
                      <span>•</span>
                      <span>{{ upload.size }}</span>
                    </div>
                  </div>
                  
                  <button
                    @click="deleteUpload(upload.id)"
                    class="text-destructive hover:text-destructive-foreground transition-all duration-300 p-1 rounded-md opacity-0 group-hover:opacity-100 hover:bg-destructive/10"
                  >
                    <Trash2 class="w-5 h-5" />
                  </button>
                </div>
                
                <div v-if="filteredUploads.length === 0" class="text-center text-muted-foreground py-8 animate-pulse">
                  {{ searchQuery ? 'No matching uploads found' : 'No uploads yet' }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 animate-slide-up">
        <div class="bg-card p-4 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 hover:scale-[1.02] border border-gray-600">
          <h3 class="text-lg font-semibold mb-2 text-primary">Total Uploads</h3>
          <p class="text-3xl font-bold">{{ stats.totalUploads }}</p>
        </div>
        
        <div class="bg-card p-4 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 hover:scale-[1.02] border border-gray-600">
          <h3 class="text-lg font-semibold mb-2 text-primary">PDF Files</h3>
          <p class="text-3xl font-bold">{{ stats.pdfCount }}</p>
        </div>
        
        <div class="bg-card p-4 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 hover:scale-[1.02] border border-gray-600">
          <h3 class="text-lg font-semibold mb-2 text-primary">Text Files</h3>
          <p class="text-3xl font-bold">{{ stats.textCount }}</p>
        </div>
        
        <div class="bg-card p-4 rounded-lg shadow-md hover:shadow-lg transition-all duration-300 hover:scale-[1.02] border border-gray-600">
          <h3 class="text-lg font-semibold mb-2 text-primary">Other Files</h3>
          <p class="text-3xl font-bold">{{ stats.otherCount }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: hsl(var(--primary)) transparent;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: hsl(var(--primary));
  border-radius: 3px;
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-out {
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}

@keyframes bounce-slow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-slide-up {
  animation: slide-up 0.5s ease-out;
}

.animate-slide-down {
  animation: slide-down 0.5s ease-out;
}

.animate-slide-out {
  animation: slide-out 0.3s ease-out forwards;
}

.animate-bounce-slow {
  animation: bounce-slow 3s infinite;
}
</style>
