<script setup>
import { ref, nextTick, watch } from 'vue';
import axios from 'axios';
import { PaperAirplaneIcon, UserIcon, CpuChipIcon } from '@heroicons/vue/24/solid';

const messages = ref([
  { role: 'assistant', content: '¡Hola! Soy tu asistente veterinario IA. ¿En qué puedo ayudarte hoy con la salud de los animales?' }
]);
const userInput = ref('');
const loading = ref(false);
const chatContainer = ref(null);

const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight;
  }
};

const sendMessage = async () => {
  if (!userInput.value.trim() || loading.value) return;

  const content = userInput.value;
  messages.value.push({ role: 'user', content });
  userInput.value = '';
  loading.value = true;
  await scrollToBottom();

  try {
    const response = await axios.post('http://localhost:8000/api/ai/chat', {
      messages: messages.value
    });
    
    messages.value.push({ role: 'assistant', content: response.data.response });
  } catch (err) {
    console.error('Error in chat:', err);
    messages.value.push({ role: 'assistant', content: 'Lo siento, tuve un problema al procesar tu consulta. Por favor intenta de nuevo.' });
  } finally {
    loading.value = false;
    await scrollToBottom();
  }
};
</script>

<template>
  <div class="flex flex-col h-[calc(100vh-10rem)] bg-white rounded-lg shadow-md overflow-hidden">
    <!-- Chat Header -->
    <div class="bg-indigo-600 p-4 text-white flex items-center">
      <CpuChipIcon class="h-6 w-6 mr-2" />
      <h2 class="text-lg font-medium">Asistente Veterinario IA</h2>
    </div>

    <!-- Chat Messages -->
    <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
      <div 
        v-for="(msg, index) in messages" 
        :key="index" 
        class="flex"
        :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div 
          class="max-w-[80%] rounded-lg px-4 py-3 shadow-sm flex items-start"
          :class="msg.role === 'user' ? 'bg-indigo-600 text-white rounded-br-none' : 'bg-white text-gray-800 border border-gray-200 rounded-bl-none'"
        >
          <UserIcon v-if="msg.role === 'user'" class="h-5 w-5 mr-2 mt-1 opacity-75 flex-shrink-0" />
          <CpuChipIcon v-else class="h-5 w-5 mr-2 mt-1 text-indigo-600 flex-shrink-0" />
          <p class="text-sm leading-relaxed">{{ msg.content }}</p>
        </div>
      </div>
      
      <div v-if="loading" class="flex justify-start">
        <div class="bg-white border border-gray-200 rounded-lg rounded-bl-none px-4 py-3 shadow-sm">
          <div class="flex space-x-2">
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Input Area -->
    <div class="p-4 bg-white border-t border-gray-200">
      <form @submit.prevent="sendMessage" class="flex space-x-2">
        <input 
          v-model="userInput" 
          type="text" 
          placeholder="Escribe tu consulta sobre síntomas, enfermedades, etc..." 
          class="flex-1 border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500"
          :disabled="loading"
        >
        <button 
          type="submit" 
          class="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          :disabled="loading || !userInput.trim()"
        >
          <PaperAirplaneIcon class="h-5 w-5 transform rotate-90" />
        </button>
      </form>
    </div>
  </div>
</template>
