<script setup>
  import { ref, computed, nextTick, onBeforeMount } from 'vue';
  import { useStore } from 'vuex';

  import {
    MessageCircle,
    Bot,
    X,
    Send,
    Download,
    Trash2,
  } from 'lucide-vue-next';
  
import axios from 'axios'
 const store=useStore()

  const isOpen = ref(false);
  const activeTab = ref('Chat');
  const currentMessage = ref('');
  const chats = ref([]);
  const chats_history = ref([]);
  const activeChat = ref(null);
  const messagesContainer = ref(null);
  const isChatStarted = ref(false); // Tracks if API was called initially
  const apiPayload = ref({})
  const newMessage = ref({})
  const historychat = ref({});
  const session_id = ref(null)
  const allChats_history =ref('')
  const currentChat = computed(() => {
    console.log(chats.value)
    return chats.value.find(chat => chat.id === activeChat.value) || null;
  });

// Define props
const props = defineProps({
  content_type: String,
  assignment_id: Number,
  question_id: Number,
  course_id: Number,
  week: Number
});

// these are the api payloads

  const generateApiPayload = () => {
    const payload = {
      query: currentMessage.value,
      tag: `${props.course_id}-${props.week}-${props.assignment_id}`,
    };

    // Add question_id to tag if content_type is "practice-assignment"
    if (props.content_type === "practice-assignment") {
      payload.tag += `-${props.question_id}`;
    }

    console.log("Generated API Payload:", payload);
    return payload;
  };

// this is this api to get history chats
  
  async function getChatHistory(){

    const response = await axios.get(`http://127.0.0.1:5000/chats/${props.course_id}`,
      {
        headers: {
          'Authentication-Token': store.state.user.token,
        },
      }
  )
      chats_history.value = response.data.data.sort((b, a) => a.id - b.id);
  }

// this is this api to get history chats
  
  async function getChats_on_history(){

  const response = await axios.get(`http://127.0.0.1:5000/chats/${props.course_id}/${historychat.value}`,
    {
      headers: {
        'Authentication-Token': store.state.user.token,
      },
    }
  )
    allChats_history.value = response.data.data;
  }

// this api is for continue chat ----------------------------------------------------------------

  async function ContinueChat(newchat) {

  try {
    const response = await axios.post(
      `http://127.0.0.1:5000/chats/${props.course_id}/${session_id.value}`, apiPayload.value,
      {
        headers: {
          "Authentication-Token": store.state.user.token,
        },
      }
    );

    // Assign aiResponse correctly using a reactive variable
    const aiResponse = {
      id: Math.random().toString(36).substring(7),
      content: response.data.data.message,
      role: 'assistant',
      timestamp: new Date(),
    };

    const chat = chats.value.find(c => c.id === activeChat.value);

    if (chat) {
      chat.messages.push(newMessage.value, aiResponse);
      getChatHistory()
    }

  } catch (error) {
    console.error("Error submitting assignment:", error);
  }
}

// ---------------------------------------------------------------------------------------------------


const handleNewMessage = () => {
  if (!currentMessage.value.trim()) return;

  newMessage.value = {
    id: Math.random().toString(36).substring(7),
    content: currentMessage.value,
    role: 'user',
    timestamp: new Date(),
  };

  apiPayload.value = generateApiPayload();

  if (!isChatStarted.value) {

    // First message: Make API call
    axios.post(
      `http://127.0.0.1:5000/chats/${props.course_id}`, apiPayload.value,
      {
        headers: {
          'Authentication-Token': store.state.user.token,
        },
      }
    )
    .then((Response) => {

      const aiResponse = {
        id: Math.random().toString(36).substring(7),
        content: Response.data.data.message,
        role: 'assistant',
        timestamp: new Date(),
      };

      session_id.value = Response.data.data.session_id;
      isChatStarted.value = true; // Set flag to true after first API call

      // Create a new chat if none is active
      const newChat = {
        id: Math.random().toString(36).substring(7),
        messages: [newMessage.value, aiResponse],
        title: session_id.value,
        timestamp: new Date(),
      };

      chats.value.push(newChat);
      activeChat.value = newChat.id;
      getChatHistory()

      // Clear input field & scroll down
      scrollToBottom();
    })
    .catch((error) => {
      console.log("Error:", error.message);
    });

  } else {
    ContinueChat();
  }
  // Clear the input field
  currentMessage.value = '';
  scrollToBottom();
};

// Function to scroll chat container to bottom
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};
  

  async function api_download(sessionId) {
  try {
      const response = await axios.put(
        `http://127.0.0.1:5000/chats/${props.course_id}/${sessionId}`,
        {}, // Empty body (if not needed)
        {
          headers: {
            'Authentication-Token': store.state.user.token,
          },
        }
      );
      console.log(response.data);
    } catch (error) {
      console.error("Error downloading chat:", error.response?.data || error.message);
    }
  }

  const downloadChat = (session_id) => {
    // const chat = chats.value.find(c => c.id === chatId);
    // if (!chat) return;
  
    // const content = chat.messages
    //   .map(m => `${m.role}: ${m.content}\n`)
    //   .join('\n');
    
    // const blob = new Blob([content], { type: 'text/plain' });
    // const url = URL.createObjectURL(blob);
    // const a = document.createElement('a');
    // a.href = url;
    // a.download = `chat-${chat.title}.txt`;
    // document.body.appendChild(a);
    // a.click();
    // document.body.removeChild(a);
    // URL.revokeObjectURL(url);
    api_download(session_id)
  };

  async function api_deleteChat(sessionId){

    const response = await axios.delete(`http://127.0.0.1:5000/chats/${props.course_id}/${sessionId}`,
      {
        headers: {
          'Authentication-Token': store.state.user.token,
        },
      }
    )
      console.log(response.data.status.message);
      getChatHistory()
  }

  const deleteChat = (session_id) => {
    api_deleteChat(session_id)
  };

  
  const continueChat = (sessionId) => {

    historychat.value = sessionId
    getChats_on_history()
    activeTab.value = 'Chat';
  };

  onBeforeMount(getChatHistory);
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
                {{ props.content_type }}
                {{ props.assignment_id }}
                {{ props.question_id }}
                {{ props.course_id }}
                {{ props.week }}
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
                <div v-if="session_id === historychat || Object.keys(historychat).length === 0">
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
                      <!-- {{ message.content }} -->
                      <span v-html=" message.content"></span>
                    </div>
                  </div>
                </div>

                <div v-else>
                  <div
                    v-for="message in allChats_history?.chat"
                    :key="message.id"
                    :class="{
                      'flex justify-end': message.role === 'user',
                      'flex justify-start': message.role === 'agent'
                    }"
                  >
                    <div
                      class="rounded-lg px-3 py-2 max-w-[85%] shadow-md transition-all duration-200 hover:scale-[1.02]"
                      :class="{
                        'bg-primary text-primary-foreground': message.role === 'user',
                        'bg-accent text-accent-foreground': message.role === 'agent'
                      }"
                    >
                      <!-- {{ message.content }} -->
                      <span v-html=" message.message"></span>
                    </div>
                  </div>
                </div>
              </div>
  
              <!-- Input -->
              <div class="border-t border-border/40 p-3 bg-accent/30">
                <div class="flex gap-2" v-if="historychat === session_id || Object.keys(historychat).length === 0">
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
                v-for="chat in chats_history"
                :key="chat.id"
                class="rounded-lg border border-border/40 p-3 bg-accent/30 hover:bg-accent/50 transition-all duration-200 hover:scale-[1.02]"
              >
                <div class="flex items-center justify-between mb-2">
                  <h3 class="font-medium text-primary text-sm">{{ chat.title }}</h3>
                  <div class="flex gap-1">
                    <button
                      @click="downloadChat(chat.session_id)"
                      class="p-1.5 hover:bg-muted/50 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50"
                      title="Download chat"
                    >
                      <Download class="h-4 w-4 text-primary" />
                    </button>
                    <button
                      @click="deleteChat(chat.session_id)"
                      class="p-1.5 hover:bg-destructive/20 rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-destructive/50"
                      title="Delete chat"
                    >
                      <Trash2 class="h-4 w-4 text-destructive" />
                    </button>
                  </div>
                </div>
                <p class="text-xs text-muted-foreground">
                  Chat {{ chat.id }} 
                </p>
                <p class="text-xs text-muted-foreground">
                  {{ chat.session_id }} 
                </p>
                <p class="text-xs text-muted-foreground">
                  {{ chat.time }} 
                </p>

                  <button
                    @click="continueChat(chat.session_id)"
                    class="mt-2 w-full rounded-md px-3 py-1.5 bg-accent hover:bg-accent/70 transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50 text-primary text-sm"
                  >
                    <div v-if="chat.session_id === session_id" class="text-red-500">
                      Current Chat
                    </div>
                    <div v-else>
                      Chat History
                    </div>
                  </button>
                </div>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </template>
  