<script setup>
  import { ref, computed } from 'vue';
  import {
    MessageCircle,
    Bot,
    X,
    Send,
    Download,
    Trash2,
  } from 'lucide-vue-next';
  
  const isOpen = ref(false);
  const activeTab = ref('Chat');
  const currentMessage = ref('');
  const chats = ref([]);
  const activeChat = ref(null);
  const messagesContainer = ref(null);
  
  const currentChat = computed(() => {
    return chats.value.find(chat => chat.id === activeChat.value) || null;
  });

  defineProps({
    content_type: String,
    assignment_id: Number,
    question_id: Number,

  });
  
  const handleNewMessage = () => {
    if (!currentMessage.value.trim()) return;
  
    const newMessage = {
      id: Math.random().toString(36).substring(7),
      content: currentMessage.value,
      role: 'user',
      timestamp: new Date(),
    };
  
    // Mock AI response
    const aiResponse = {
      id: Math.random().toString(36).substring(7),
      content: 'This is a mock AI response. In a real implementation, this would be connected to an AI service.',
      role: 'assistant',
      timestamp: new Date(),
    };
  
    if (!activeChat.value) {
      const newChat = {
        id: Math.random().toString(36).substring(7),
        messages: [newMessage, aiResponse],
        title: `Chat ${chats.value.length + 1}`,
        timestamp: new Date(),
      };
      chats.value.push(newChat);
      activeChat.value = newChat.id;
    } else {
      const chat = chats.value.find(c => c.id === activeChat.value);
      if (chat) {
        chat.messages.push(newMessage, aiResponse);
      }
    }
  
    currentMessage.value = '';
    
    // Scroll to bottom after messages update
    setTimeout(() => {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
      }
    }, 0);
  };
  
  const downloadChat = (chatId) => {
    const chat = chats.value.find(c => c.id === chatId);
    if (!chat) return;
  
    const content = chat.messages
      .map(m => `${m.role}: ${m.content}\n`)
      .join('\n');
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `chat-${chat.title}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };
  
  const deleteChat = (chatId) => {
    chats.value = chats.value.filter(chat => chat.id !== chatId);
    if (activeChat.value === chatId) {
      activeChat.value = null;
    }
  };
  
  const continueChat = (chatId) => {
    activeChat.value = chatId;
    activeTab.value = 'Chat';
  };
  </script>

<template>
    <div>
      <!-- Chat Button with Pulse Effect -->
      <button
        @click="isOpen = true"
        class="fixed bottom-4 right-12 h-14 w-14 rounded-full bg-accent hover:bg-accent/90 text-accent-foreground shadow-lg transition-all duration-200 hover:scale-105 focus:outline-none focus:ring-2 focus:ring-primary/50 group"
      >
        <MessageCircle class="h-6 w-6 mx-auto transition-transform group-hover:scale-110" />
        <span class="absolute -top-1 -right-1 h-3 w-3">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
          <span class="relative inline-flex rounded-full h-3 w-3 bg-primary"></span>
        </span>
      </button>
  
      <!-- Chat Panel -->
      <Transition name="slide">
        <div
          v-if="isOpen"
          class="fixed bottom-3 right-4 w-[520px] h-[680px] bg-background rounded-lg shadow-xl flex flex-col z-50 overflow-hidden border border-border/40"
        >
          <!-- Header -->
          <div class="border-b border-border/40 p-3 bg-accent/50">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="relative">
                  <Bot class="h-5 w-5 text-primary" />
                  <span class="absolute -top-1 -right-1 h-2 w-2 bg-primary rounded-full"></span>
                </div>
                <h2 class="text-base font-semibold text-primary">AI Assistant</h2>
                {{ content_type }}
                {{ assignment_id }}
                {{ question_id }}
              </div>
              <button
                @click="isOpen = false"
                class="rounded-full p-1.5 hover:bg-muted/50 transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50"
              >
                <X class="h-4 w-4 text-primary" />
              </button>
            </div>
          </div>
  
          <!-- Tabs -->
          <div class="border-b border-border/40 bg-accent/30">
            <div class="flex">
              <button
                v-for="tab in ['Chat', 'History']"
                :key="tab"
                @click="activeTab = tab"
                class="flex-1 px-3 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-primary/50"
                :class="{
                  'border-b-2 border-primary text-primary': activeTab === tab,
                  'text-muted-foreground hover:text-primary/80': activeTab !== tab
                }"
              >
                {{ tab }}
              </button>
            </div>
          </div>
  
          <!-- Content -->
          <div class="flex-1 overflow-hidden">
            <!-- Chat Tab -->
            <div v-if="activeTab === 'Chat'" class="h-full flex flex-col">
              <!-- Messages -->
              <div
                ref="messagesContainer"
                class="flex-1 overflow-y-auto p-3 space-y-3 scrollbar-thin scrollbar-thumb-accent scrollbar-track-transparent"
              >
                <div
                  v-for="message in currentChat?.messages"
                  :key="message.id"
                  :class="{
                    'flex justify-end': message.role === 'user',
                    'flex justify-start': message.role === 'assistant'
                  }"
                >
                  <div
                    class="rounded-lg px-3 py-2 max-w-[85%] shadow-md transition-all duration-200 hover:scale-[1.02]"
                    :class="{
                      'bg-primary text-primary-foreground': message.role === 'user',
                      'bg-accent text-accent-foreground': message.role === 'assistant'
                    }"
                  >
                    {{ message.content }}
                  </div>
                </div>
              </div>
  
              <!-- Input -->
              <div class="border-t border-border/40 p-3 bg-accent/30">
                <div class="flex gap-2">
                  <input
                    v-model="currentMessage"
                    @keyup.enter="handleNewMessage"
                    type="text"
                    placeholder="Type your message..."
                    class="flex-1 rounded-md border border-border/40 bg-accent/50 px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50 placeholder:text-muted-foreground"
                  />
                  <button
                    @click="handleNewMessage"
                    class="rounded-md bg-primary px-3 py-1.5 text-primary-foreground hover:bg-primary/90 transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50 disabled:opacity-50"
                    :disabled="!currentMessage.trim()"
                  >
                    <Send class="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
  
            <!-- History Tab -->
            <div
              v-else
              class="h-full overflow-y-auto p-3 space-y-3 scrollbar-thin scrollbar-thumb-accent scrollbar-track-transparent"
            >
              <div
                v-for="chat in chats"
                :key="chat.id"
                class="rounded-lg border border-border/40 p-3 bg-accent/30 hover:bg-accent/50 transition-all duration-200 hover:scale-[1.02]"
              >
                <div class="flex items-center justify-between mb-2">
                  <h3 class="font-medium text-primary text-sm">{{ chat.title }}</h3>
                  <div class="flex gap-1">
                    <button
                      @click="downloadChat(chat.id)"
                      class="p-1.5 hover:bg-muted/50 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50"
                      title="Download chat"
                    >
                      <Download class="h-4 w-4 text-primary" />
                    </button>
                    <button
                      @click="deleteChat(chat.id)"
                      class="p-1.5 hover:bg-destructive/20 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-destructive/50"
                      title="Delete chat"
                    >
                      <Trash2 class="h-4 w-4 text-destructive" />
                    </button>
                  </div>
                </div>
                <p class="text-xs text-muted-foreground">
                  {{ chat.messages.length }} messages
                </p>
                <button
                  @click="continueChat(chat.id)"
                  class="mt-2 w-full rounded-md px-3 py-1.5 bg-accent hover:bg-accent/70 transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50 text-primary text-sm"
                >
                  Continue Chat
                </button>
              </div>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </template>
  