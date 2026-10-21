<script setup>
  import { ref } from 'vue';
  import { ArrowLeft, Download, FileText } from 'lucide-vue-next';
  import { useMotion } from '@vueuse/motion';
  
  const documents = ref([
    {
      id: 1,
      name: 'Annual Report 2024',
      type: 'PDF Document',
      date: '2024-03-15',
      imageUrl: 'https://images.unsplash.com/photo-1589330694653-ded6df03f754?w=800&auto=format&fit=crop',
    },
    {
      id: 2,
      name: 'Financial Statement',
      type: 'PDF Document',
      date: '2024-03-10',
      imageUrl: 'https://images.unsplash.com/photo-1618005198919-d3d4b5a92ead?w=800&auto=format&fit=crop',
    },
    {
      id: 3,
      name: 'Project Proposal',
      type: 'PDF Document',
      date: '2024-03-05',
      imageUrl: 'https://images.unsplash.com/photo-1585909695284-32d2985ac9c0?w=800&auto=format&fit=crop',
    },
  ]);
  
  const selectedDoc = ref(null);
  const downloadingId = ref(null);
  
  const handleDownload = async (doc) => {
    downloadingId.value = doc.id;
    try {
      const link = document.createElement('a');
      link.href = doc.imageUrl;
      link.download = `${doc.name}.jpg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } finally {
      setTimeout(() => (downloadingId.value = null), 1000);
    }
  };
  </script>

<template>
    <Transition
      mode="out-in"
      enter-active-class="transition-all duration-300 ease-out"
      enter-from-class="opacity-0 translate-y-4"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-300 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 translate-y-4"
    >
      <div v-if="selectedDoc" key="document-view" class="min-h-screen bg-background p-8">
        <div class="max-w-6xl mx-auto">
          <button
            class="inline-flex items-center px-4 py-2 text-sm font-medium transition-colors rounded-md hover:bg-accent hover:text-accent-foreground mb-6 group"
            @click="selectedDoc = null"
          >
            <ArrowLeft class="mr-2 h-4 w-4 transition-transform group-hover:-translate-x-1" />
            Back to Documents
          </button>
          
          <div
            class="overflow-hidden rounded-lg border bg-card text-card-foreground shadow-lg"
            useMotion
            :initial="{ scale: 0.95, opacity: 0 }"
            :enter="{ scale: 1, opacity: 1 }"
            :transition="{ delay: 200 }"
          >
            <div class="bg-muted p-4 border-b">
              <h2 class="text-xl font-semibold">{{ selectedDoc.name }}</h2>
              <p class="text-sm text-muted-foreground">{{ selectedDoc.type }} • {{ selectedDoc.date }}</p>
            </div>
            <div class="relative group">
              <img :src="selectedDoc.imageUrl" :alt="selectedDoc.name" class="w-full h-auto" />
              <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <button
                  class="inline-flex items-center px-4 py-2 text-sm font-medium transition-all bg-primary text-primary-foreground hover:bg-primary/90 rounded-md transform scale-95 hover:scale-100"
                  @click="handleDownload(selectedDoc)"
                >
                  <Download class="mr-2 h-4 w-4" />
                  Download Document
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <div v-else key="document-list" class="min-h-screen bg-background p-8">
        <div class="max-w-6xl mx-auto">
          <div useMotion :initial="{ y: -20, opacity: 0 }" :enter="{ y: 0, opacity: 1 }" :transition="{ delay: 100 }">
            <h1 class="text-4xl font-bold mb-2">Documents</h1>
            <p class="text-muted-foreground mb-8">View and manage your important files</p>
          </div>
          
          <div class="space-y-4">
            <div v-for="(doc, index) in documents" :key="doc.id" useMotion :initial="{ x: -20, opacity: 0 }" :enter="{ x: 0, opacity: 1 }" :transition="{ delay: index * 100 }">
              <div class="group rounded-lg border bg-card text-card-foreground hover:shadow-md transition-all duration-300">
                <div class="p-4">
                  <div class="flex items-center justify-between">
                    <button @click="selectedDoc = doc" class="flex items-center space-x-4 flex-1">
                      <div class="bg-primary/5 p-2 rounded-lg group-hover:bg-primary/10 transition-colors">
                        <FileText class="h-6 w-6 text-primary" />
                      </div>
                      <div class="flex flex-col items-start">
                        <span class="font-medium group-hover:text-primary transition-colors">{{ doc.name }}</span>
                        <span class="text-sm text-muted-foreground">{{ doc.type }} • {{ doc.date }}</span>
                      </div>
                    </button>
                    
                    <button @click="handleDownload(doc)" class="p-2 rounded-md opacity-0 group-hover:opacity-100 transition-opacity hover:bg-accent hover:text-accent-foreground" :disabled="downloadingId === doc.id">
                      <Download :class="['h-4 w-4', { 'animate-bounce': downloadingId === doc.id }]" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </template>

  
  