<template>
  <div class="h-full">
  <div class="h-full flex flex-col font-sans text-slate-600 bg-slate-50/50">
    
    <div class="mb-4 shrink-0 px-1">
      <div class="flex items-end justify-between">
        <div>
          <h2 class="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <SparklesIcon class="h-6 w-6 text-indigo-600" />
            Asistente IA
          </h2>
          <p class="text-sm text-slate-500 mt-1">Consultas clínicas y apoyo diagnóstico.</p>
        </div>
        
        <div>
          <button 
            @click="loadClinicalCase"
            class="flex items-center gap-2 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold uppercase tracking-wide rounded-full shadow-md shadow-indigo-200 transition-all hover:-translate-y-0.5 active:translate-y-0"
          >
            <FolderPlusIcon class="h-4 w-4" />
            <span>Cargar Caso</span>
          </button>
        </div>
      </div>
    </div>

    <div class="flex-1 bg-white rounded-t-3xl shadow-[0_-4px_20px_rgba(0,0,0,0.02)] border border-slate-200 overflow-hidden flex flex-col min-h-0 relative">
      
      <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-[0.03] pointer-events-none"></div>

      <div ref="chatContainer" class="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 custom-scrollbar relative z-10">
        
        <div v-if="messages.length === 0" class="flex flex-col items-center justify-center h-full text-center opacity-60 space-y-4">
          <div class="w-16 h-16 bg-indigo-50 rounded-full flex items-center justify-center">
            <CpuChipIcon class="h-8 w-8 text-indigo-500" />
          </div>
          <div>
            <p class="text-slate-800 font-bold">¿En qué puedo ayudarte?</p>
            <p class="text-sm text-slate-500">Pregunta sobre síntomas, dosis o procedimientos.</p>
          </div>
        </div>

        <div 
          v-for="(msg, index) in messages" 
          :key="index" 
          class="flex w-full"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div class="flex max-w-[85%] sm:max-w-[75%] gap-3" :class="msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'">
            
            <ChatAvatar :role="msg.role" />

            <div 
              class="px-5 py-3.5 shadow-sm text-sm leading-relaxed relative group"
              :class="[
                msg.role === 'user' 
                  ? 'bg-indigo-600 text-white rounded-2xl rounded-tr-none' 
                  : 'bg-slate-50 text-slate-700 border border-slate-100 rounded-2xl rounded-tl-none'
              ]"
            >
              <div v-html="formatMessage(msg.content)" class="prose prose-sm max-w-none prose-indigo"></div>
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
            
            <ChatAvatar role="assistant" />

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
  </div>
    <!-- Case Selection Modal -->
    <div v-if="isCaseModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="closeCaseModal">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-2xl overflow-hidden flex flex-col max-h-[80vh]">
        
        <div class="bg-indigo-600 px-6 py-4 flex justify-between items-center shrink-0">
          <div>
            <h3 class="text-lg font-bold text-white flex items-center gap-2">
              <FolderPlusIcon class="h-5 w-5" />
              Solicitudes Pendientes
            </h3>
            <p class="text-indigo-100 text-xs mt-0.5">Selecciona una solicitud para analizar</p>
          </div>
          <button @click="closeCaseModal" class="text-indigo-200 hover:text-white transition-colors bg-white/10 hover:bg-white/20 p-1.5 rounded-lg">
            <XMarkIcon class="h-5 w-5"/>
          </button>
        </div>

        <div class="p-4 border-b border-slate-100 bg-slate-50 flex gap-4 shrink-0">
          <div class="flex-1 relative">
            <input 
              v-model="caseSearch"
              type="text" 
              placeholder="Buscar por paciente o síntomas..." 
              class="w-full pl-9 pr-4 py-2.5 text-sm bg-white border-0 ring-1 ring-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm text-slate-700 placeholder:text-slate-400"
            />
            <MagnifyingGlassIcon class="h-5 w-5 text-slate-400 absolute left-2.5 top-2.5" />
          </div>
        </div>

        <div class="flex-1 overflow-y-auto p-4 space-y-3 custom-scrollbar bg-slate-50/50">
          <div v-if="filteredCases.length === 0" class="flex flex-col items-center justify-center py-12 text-slate-400 opacity-60">
            <InboxIcon class="h-12 w-12 mb-2" />
            <p class="text-sm font-medium">No hay solicitudes pendientes</p>
          </div>

          <div 
            v-for="item in filteredCases" 
            :key="item.id"
            @click="selectCase(item)"
            class="bg-white p-4 rounded-xl shadow-sm hover:shadow-md hover:ring-1 hover:ring-indigo-500 transition-all cursor-pointer group relative overflow-hidden border border-transparent"
          >
            <div class="absolute left-0 top-0 bottom-0 w-1 bg-amber-500"></div>
            
            <div class="flex justify-between items-start pl-3">
              <div>
                <div class="flex items-center gap-2 mb-1">
                  <span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded-full bg-amber-50 text-amber-600">
                    Solicitud
                  </span>
                  <span class="text-xs font-mono text-slate-400">{{ item.date }}</span>
                </div>
                <h4 class="font-bold text-slate-800 text-sm">{{ item.petName }} <span class="text-slate-400 font-normal text-xs">({{ item.species }})</span></h4>
                <p class="text-xs text-slate-500 mt-1 line-clamp-2">{{ item.description }}</p>
              </div>
              
              <div v-if="item.images && item.images.length > 0" class="flex -space-x-2">
                <img 
                  v-for="(img, idx) in item.images.slice(0, 3)" 
                  :key="idx"
                  :src="`http://localhost:8000/${img}`"
                  class="w-8 h-8 rounded-full border-2 border-white object-cover shadow-sm"
                />
                <div v-if="item.images.length > 3" class="w-8 h-8 rounded-full border-2 border-white bg-slate-100 flex items-center justify-center text-[9px] font-bold text-slate-500 shadow-sm">
                  +{{ item.images.length - 3 }}
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>


<script setup>
import { ref, nextTick } from 'vue';
import axios from 'axios';
import { 
  PaperAirplaneIcon, 
  CpuChipIcon, 
  SparklesIcon, 
  FolderPlusIcon,
  XMarkIcon,
  MagnifyingGlassIcon,
  InboxIcon
} from '@heroicons/vue/24/outline';
import { useServiceRequests } from '@/composables/useServiceRequests';
import { useUserStore } from '@/stores/user';

// Importamos el nuevo componente
import ChatAvatar from '@/components/ChatAvatar.vue';

const messages = ref([
  { role: 'assistant', content: '¡Hola Dr.! Soy tu asistente veterinario. Puedo ayudarte a analizar síntomas, revisar dosis o buscar información clínica. ¿Por dónde empezamos?' }
]);
const userInput = ref('');
const loading = ref(false);
const chatContainer = ref(null);
const isCaseModalOpen = ref(false);
const caseSearch = ref('');
const requests = ref([]);
const { getAllRequests } = useServiceRequests();
const userStore = useUserStore();

const loadClinicalCase = async () => {
  isCaseModalOpen.value = true;
  loading.value = true;
  try {
    const reqData = await getAllRequests();

    requests.value = reqData.map(req => ({
      id: `req-${req.id}`,
      type: 'request',
      date: req.service_data.preferredDate ? req.service_data.preferredDate.split('T')[0] : 'Pendiente',
      petName: req.pet_name || req.service_data.petName || 'Sin nombre',
      species: req.service_data.species || 'General',
      description: req.service_data.symptoms || req.service_data.description || req.service_data.notes || 'Solicitud de servicio',
      images: req.images || []
    }));

  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

const closeCaseModal = () => {
  isCaseModalOpen.value = false;
};

const filteredCases = ref([]);

// Watchers para filtrar (usando ref simple por simplicidad en setup script)
import { watch, computed } from 'vue';

const computedFilteredCases = computed(() => {
  let list = requests.value;
  if (caseSearch.value) {
    const q = caseSearch.value.toLowerCase();
    list = list.filter(item => 
      item.petName.toLowerCase().includes(q) || 
      item.description.toLowerCase().includes(q)
    );
  }
  return list;
});

watch([caseSearch, requests], () => {
  filteredCases.value = computedFilteredCases.value;
});

const selectCase = (item) => {
  let prompt = `Actúa como un experto Veterinario Senior con especialización en medicina interna y diagnóstico por imagen. Analiza el siguiente caso clínico y proporciona tu opinión profesional.\n\n`;
  prompt += `### Información del Paciente\n`;
  prompt += `**Nombre:** ${item.petName}\n`;
  prompt += `**Especie:** ${item.species}\n`;
  prompt += `**Fecha del Caso:** ${item.date}\n\n`;
  
  prompt += `### Cuadro Clínico\n`;
  prompt += `**Descripción/Síntomas:**\n${item.description}\n\n`;
  
  if (item.images.length > 0) {
    prompt += `### Evidencia Visual\n`;
    prompt += `Se adjuntan las siguientes imágenes para tu análisis:\n`;
    item.images.forEach(img => {
      // Usamos la URL completa para que la IA (si tiene visión) pueda acceder, o para mostrarla en el chat
      prompt += `![Imagen del Caso](http://localhost:8000/${img})\n`;
    });
    prompt += `\n`;
  }

  prompt += `### Solicitud\n`;
  prompt += `Por favor, estructura tu respuesta de la siguiente manera:\n`;
  prompt += `1. **Resumen del Caso**: Breve interpretación de los datos.\n`;
  prompt += `2. **Pre-diagnóstico Diferencial**: Lista de posibles causas ordenadas por probabilidad.\n`;
  prompt += `4. **Plan Sugerido**: Pruebas diagnósticas recomendadas y tratamiento inicial.\n`;

  userInput.value = prompt;
  closeCaseModal();
  sendMessage(); // Auto-enviar
};

const formatMessage = (content) => {
  if (!content) return '';
  
  // 1. Render Images: ![alt](url)
  let formatted = content.replace(/!\[(.*?)\]\((.*?)\)/g, (match, alt, url) => {
    return `<div class="my-2"><img src="${url}" alt="${alt}" class="rounded-lg max-w-full sm:max-w-xs h-auto shadow-sm border border-slate-200 object-cover" /></div>`;
  });

  // 2. Render Headers: ### Header -> <strong>Header</strong>
  formatted = formatted.replace(/^###\s+(.*)$/gm, '<div class="font-bold text-slate-800 mt-3 mb-1 text-sm uppercase tracking-wide">$1</div>');
  formatted = formatted.replace(/^##\s+(.*)$/gm, '<div class="font-bold text-slate-800 mt-2 mb-1">$1</div>');

  // 3. Render Bold: **text**
  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  // 4. Render Lists: - item
  formatted = formatted.replace(/^\s*-\s+(.*)$/gm, '<li class="ml-4 list-disc">$1</li>');

  // 5. Render Newlines (handling lists correctly)
  formatted = formatted.replace(/\n/g, '<br>');

  return formatted;
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
</script>

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