<script setup>
import { ref, nextTick } from 'vue';
import axios from 'axios';
import { 
  PaperAirplaneIcon, 
  UserIcon, 
  CpuChipIcon, 
  SparklesIcon 
} from '@heroicons/vue/24/solid';

// Estado interno del chat
const messages = ref([
  { role: 'assistant', content: '¡Hola Dr.! Soy tu asistente veterinario. Puedo ayudarte a analizar síntomas, revisar dosis o buscar información clínica. ¿Por dónde empezamos?' }
]);
const userInput = ref('');
const loading = ref(false);
const chatContainer = ref(null);

// Método expuesto para que el padre pueda añadir mensajes (ej: "Cargando caso...")
const addSystemMessage = async (text) => {
  messages.value.push({ role: 'assistant', content: text });
  await scrollToBottom();
};

const scrollToBottom = async () => {
  await nextTick();
  if (chatContainer.value) {
    chatContainer.value.scrollTo({
      top: chatContainer.value.scrollHeight,
      behavior: 'smooth'
    });
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
    messages.value.push({ role: 'assistant', content: 'Lo siento, tuve un problema de conexión. Por favor intenta de nuevo.' });
  } finally {
    loading.value = false;
    await scrollToBottom();
  }
};

// Exponemos el método para usarlo desde fuera
defineExpose({ addSystemMessage });
</script>

<template>
  <div class="flex flex-col h-full relative overflow-hidden">
    
    <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-[0.03] pointer-events-none"></div>

    <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 custom-scrollbar relative z-10">
      
      <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-center opacity-60 space-y-4">
        <div class="w-16 h-16 bg-indigo-50 rounded-full flex items-center justify-center">
          <CpuChipIcon class="h-8 w-8 text-indigo-500" />
        </div>
        <div>
          <p class="text-slate-800 font-bold">Asistente Listo</p>
          <p class="text-sm text-slate-500">Esperando consulta...</p>
        </div>
      </div>

      <div 
        v-for="(msg, index) in messages" 
        :key="index" 
        class="flex w-full"
        :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div class="flex max-w-[85%] sm:max-w-[75%] gap-3" :class="msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'">
          
          <div class="shrink-0 h-8 w-8 rounded-full flex items-center justify-center shadow-sm border" 
            :class="msg.role === 'user' ? 'bg-indigo-100 border-indigo-200' : 'bg-emerald-50 border-emerald-100'">
            <UserIcon v-if="msg.role === 'user'" class="h-4 w-4 text-indigo-700" />
            <SparklesIcon v-else class="h-4 w-4 text-emerald-600" />
          </div>

          <div 
            class="px-5 py-3.5 shadow-sm text-sm leading-relaxed relative group"
            :class="[
              msg.role === 'user' 
                ? 'bg-indigo-600 text-white rounded-2xl rounded-tr-none' 
                : 'bg-slate-50 text-slate-700 border border-slate-100 rounded-2xl rounded-tl-none'
            ]"
          >
            <p>{{ msg.content }}</p>
            <span class="text-[9px] absolute -bottom-5 opacity-0 group-hover:opacity-100 transition-opacity text-slate-400 w-20"
              :class="msg.role === 'user' ? 'right-0 text-right' : 'left-0 text-left'"
            >
              Hace un momento
            </span>
          </div>
        </div>
      </div>

      <div v-if="loading" class="flex justify-start w-full">
        <div class="flex gap-3 max-w-[75%]">
          <div class="shrink-0 h-8 w-8 rounded-full bg-emerald-50 border border-emerald-100 flex items-center justify-center shadow-sm">
            <SparklesIcon class="h-4 w-4 text-emerald-600" />
          </div>
          <div class="bg-slate-50 border border-slate-100 px-4 py-3 rounded-2xl rounded-tl-none flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></span>
            <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-100"></span>
            <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-200"></span>
          </div>
        </div>
      </div>

    </div>

    <div class="p-4 bg-white border-t border-slate-100 z-20">
      <form @submit.prevent="sendMessage" class="relative flex items-end gap-2 max-w-4xl mx-auto">
        <div class="relative flex-1">
          <input 
            v-model="userInput" 
            type="text" 
            placeholder="Escribe tu consulta veterinaria..." 
            class="w-full pl-5 pr-12 py-3.5 bg-slate-50 border border-slate-200 rounded-full text-sm text-slate-700 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all shadow-inner"
            :disabled="loading"
          >
          <div class="absolute right-4 top-1/2 -translate-y-1/2 text-slate-300 pointer-events-none">
            <CpuChipIcon class="h-5 w-5" />
          </div>
        </div>

        <button 
          type="submit" 
          class="h-[46px] w-[46px] flex items-center justify-center rounded-full bg-indigo-600 text-white shadow-md hover:bg-indigo-700 hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0 transition-all duration-200"
          :disabled="loading || !userInput.trim()"
        >
          <PaperAirplaneIcon class="h-5 w-5 transform -rotate-45 translate-x-0.5 -translate-y-0.5" />
        </button>
      </form>
      
      <p class="text-center text-[10px] text-slate-400 mt-2">
        La IA puede cometer errores. Verifica la información clínica importante.
      </p>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
.delay-100 { animation-delay: 150ms; }
.delay-200 { animation-delay: 300ms; }
</style>