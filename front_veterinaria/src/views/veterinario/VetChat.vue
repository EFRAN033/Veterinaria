<template>
  <div class="h-full">
  <div class="h-full flex flex-col font-sans text-slate-600 bg-slate-50/50">
    
    <div class="mb-4 shrink-0 px-1">
      <div class="flex items-end justify-between">
        <div>
          <h2 class="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <SparklesIcon class="h-6 w-6 text-indigo-600" />
            Asistente IA
            <span v-if="currentCategory !== 'GENERAL'" class="text-[10px] bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full uppercase tracking-wider border border-indigo-200">{{ currentCategory }}</span>
          </h2>
          <p class="text-sm text-slate-500 mt-1">Consultas clínicas y apoyo diagnóstico.</p>
        </div>
        
        <div class="flex items-center gap-3">
          <button 
            @click="generateReport"
            :disabled="messages.length < 2 || generatingReport"
            class="flex items-center gap-2 px-4 py-2 bg-white border border-slate-200 text-slate-700 rounded-xl hover:bg-slate-50 hover:border-slate-300 transition-all text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <DocumentTextIcon class="h-5 w-5 text-indigo-600" />
            <span v-if="generatingReport">Generando...</span>
            <span v-else>Generar Reporte</span>
          </button>

          <button 
            @click="loadClinicalCase"
            class="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200 text-sm font-medium"
          >
            <FolderPlusIcon class="h-5 w-5" />
            Cargar Caso
          </button>
        </div>
      </div>
    </div>

    <div class="flex-1 flex gap-4 overflow-hidden min-h-0">
      
      <!-- Chat Area -->
      <div class="flex-1 bg-white rounded-3xl shadow-[0_-4px_20px_rgba(0,0,0,0.02)] border border-slate-200 overflow-hidden flex flex-col relative">
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
              
              <ChatAvatar 
                :role="msg.role" 
                :isAnimated="index === messages.length - 1 && msg.role === 'assistant'"
                :isLatest="index === messages.length - 1"
              />

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
              <ChatAvatar role="assistant" :isAnimated="true" :isLatest="true" />
              <div class="bg-slate-50 border border-slate-100 px-4 py-3 rounded-2xl rounded-tl-none flex items-center gap-1.5">
                <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></span>
                <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-100"></span>
                <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce delay-200"></span>
              </div>
            </div>
          </div>

        </div>

        <div class="p-4 bg-white border-t border-slate-100 z-20">
          <form @submit.prevent="sendMessage" class="flex gap-3 items-end">
            <!-- Image Preview -->
            <div v-if="selectedImagePreview" class="absolute bottom-full mb-2 left-0 bg-white p-2 rounded-xl shadow-lg border border-slate-200 animate-fade-in-up">
              <div class="relative">
                <img :src="selectedImagePreview" class="h-20 w-20 object-cover rounded-lg" />
                <button @click="clearImage" type="button" class="absolute -top-2 -right-2 bg-rose-500 text-white rounded-full p-1 shadow-sm hover:bg-rose-600">
                  <XMarkIcon class="h-3 w-3" />
                </button>
              </div>
            </div>

            <!-- Quick Actions -->
            <div class="absolute bottom-full mb-3 left-0 right-0 flex gap-2 overflow-x-auto pb-2 px-1 custom-scrollbar-hide mask-fade-sides">
              <button 
                v-for="action in quickActions" 
                :key="action"
                type="button"
                @click="useQuickAction(action)"
                class="whitespace-nowrap px-3 py-1.5 bg-white border border-indigo-100 text-indigo-600 text-xs font-bold rounded-lg shadow-sm hover:bg-indigo-50 hover:border-indigo-200 transition-all active:scale-95"
              >
                {{ action }}
              </button>
            </div>

            <div class="relative flex-1">
              <!-- Ghost Text Overlay -->
              <div class="absolute inset-0 pl-12 py-3.5 text-sm pointer-events-none overflow-hidden whitespace-pre">
                <span class="invisible">{{ userInput }}</span><span class="text-slate-400 opacity-60">{{ suggestionSuffix }}</span>
              </div>

              <input 
                v-model="userInput" 
                @input="checkAutocomplete"
                @keydown="handleKeydown"
                type="text" 
                placeholder="Escribe tu consulta veterinaria..." 
                class="w-full pl-12 pr-12 py-3.5 bg-slate-50 border border-slate-200 rounded-full text-sm text-slate-700 placeholder-slate-400 focus:outline-none focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 transition-all shadow-inner relative z-10 bg-transparent"
                :disabled="loading"
              >
              <!-- Image Upload Button -->
              <div class="absolute left-2 top-1/2 -translate-y-1/2">
                <button 
                  type="button"
                  @click="$refs.fileInput.click()"
                  class="p-2 text-slate-400 hover:text-indigo-600 transition-colors rounded-full hover:bg-slate-100"
                  title="Adjuntar imagen clínica"
                >
                  <PaperClipIcon class="h-5 w-5" />
                </button>
                <input 
                  ref="fileInput"
                  type="file" 
                  accept="image/*" 
                  class="hidden"
                  @change="handleImageUpload"
                >
              </div>
              
              <div class="absolute right-4 top-1/2 -translate-y-1/2 flex items-center gap-2">
                <!-- Voice Input -->
                <button 
                  type="button"
                  @click="toggleVoiceRecording"
                  class="p-1.5 rounded-full transition-all duration-300"
                  :class="isRecording ? 'bg-rose-100 text-rose-600 animate-pulse' : 'text-slate-300 hover:text-indigo-600 hover:bg-slate-100'"
                  title="Dictado por voz"
                >
                  <MicrophoneIcon class="h-5 w-5" />
                </button>
                <CpuChipIcon class="h-5 w-5 text-slate-300" />
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

      <!-- Clinical Insights Panel -->
      <ClinicalInsights 
        :insights="clinicalInsights" 
        @schedule="handleSchedule"
      />


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
                  :src="`${backendUrl}/${img}`"
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

    <!-- Report Modal -->
    <div v-if="showReportModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="showReportModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-3xl max-h-[85vh] flex flex-col overflow-hidden animate-fade-in-up">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h3 class="text-xl font-bold text-slate-800 flex items-center gap-2">
            <DocumentTextIcon class="h-6 w-6 text-indigo-600" />
            Reporte Clínico Generado
          </h3>
          <button @click="showReportModal = false" class="text-slate-400 hover:text-slate-600 transition-colors">
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
        
        <div class="p-8 overflow-y-auto custom-scrollbar bg-white">
          <div class="prose prose-slate max-w-none prose-headings:text-indigo-900 prose-a:text-indigo-600">
            <div v-html="formatMessage(reportContent)"></div>
          </div>
        </div>

        <div class="p-4 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
          <button @click="showReportModal = false" class="px-4 py-2 text-slate-600 font-medium hover:bg-slate-200 rounded-lg transition-colors">
            Cerrar
          </button>
          <button @click="downloadReport" class="px-4 py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors flex items-center gap-2">
            <ArrowDownTrayIcon class="h-5 w-5" />
            Descargar Markdown
          </button>
        </div>
      </div>
    </div>

    <!-- Schedule Modal -->
    <div v-if="showScheduleModal" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="showScheduleModal = false">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] flex flex-col overflow-hidden animate-fade-in-up">
        <div class="p-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <h3 class="text-xl font-bold text-slate-800 flex items-center gap-2">
            <CalendarDaysIcon class="h-6 w-6 text-indigo-600" />
            Agendar Seguimiento
          </h3>
          <button @click="showScheduleModal = false" class="text-slate-400 hover:text-slate-600 transition-colors">
            <XMarkIcon class="h-6 w-6" />
          </button>
        </div>
        
        <div class="p-8 overflow-y-auto custom-scrollbar bg-white">
          <DateTimePicker v-model="appointmentData" mode="vet" :takenSlots="takenSlots" />
          
          <div class="mt-6">
            <label class="block text-sm font-bold text-slate-700 mb-2">Notas Adicionales</label>
            <textarea 
              v-model="scheduleNotes"
              rows="3"
              class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-all text-sm"
              placeholder="Detalles adicionales para la cita..."
            ></textarea>
          </div>
        </div>

        <div class="p-4 border-t border-slate-100 bg-slate-50 flex justify-end gap-3">
          <button @click="showScheduleModal = false" class="px-4 py-2 text-slate-600 font-medium hover:bg-slate-200 rounded-lg transition-colors">
            Cancelar
          </button>
          <button 
            @click="confirmAppointment" 
            class="px-6 py-2 bg-indigo-600 text-white font-bold rounded-lg hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200 flex items-center gap-2"
            :disabled="loading"
          >
            <span v-if="loading" class="animate-spin">⌛</span>
            Confirmar Cita
          </button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, nextTick, computed, watch, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { 
  PaperAirplaneIcon, 
  CpuChipIcon, 
  SparklesIcon, 
  FolderPlusIcon,
  XMarkIcon,
  MagnifyingGlassIcon,
  InboxIcon,
  DocumentTextIcon,
  ArrowDownTrayIcon,
  PaperClipIcon,
  MicrophoneIcon,
  CalendarDaysIcon
} from '@heroicons/vue/24/outline';
import { useServiceRequests } from '@/composables/useServiceRequests';
import { usePets } from '@/composables/usePets';
import { useUserStore } from '@/stores/user';

import ChatAvatar from '@/components/ChatAvatar.vue';
import ClinicalInsights from '@/components/ClinicalInsights.vue';
import DateTimePicker from '@/components/DateTimePicker.vue';
import { useToast } from '@/composables/useToast';

const { addToast } = useToast();

const messages = ref([
  { role: 'assistant', content: '¡Hola Dr.! Soy tu asistente veterinario. Puedo ayudarte a analizar síntomas, revisar dosis o buscar información clínica. ¿Por dónde empezamos?' }
]);
const userInput = ref('');
const loading = ref(false);
const chatContainer = ref(null);
const isCaseModalOpen = ref(false);
const caseSearch = ref('');
const requests = ref([]);
const { getAllRequests, getRequestById } = useServiceRequests();
const { getPetsByUserId } = usePets();
const userStore = useUserStore();
const backendUrl = import.meta.env.VITE_BACKEND_URL;
const route = useRoute();

// New state for AI enhancements
const currentCategory = ref('GENERAL');
const clinicalInsights = ref(null);

const quickActions = [
  'Diagnóstico Diferencial',
  'Plan Terapéutico',
  'Dosis Farmacológica',
  'Interpretación Labs',
  'Protocolo de Vacunación'
];

import { veterinaryDictionary } from '@/data/veterinaryDictionary';

const commonPhrases = veterinaryDictionary;

const suggestionSuffix = ref('');

const checkAutocomplete = () => {
  const input = userInput.value.toLowerCase();
  if (!input) {
    suggestionSuffix.value = '';
    return;
  }

  const match = commonPhrases.find(phrase => 
    phrase.toLowerCase().startsWith(input) && phrase.length > input.length
  );

  if (match) {
    // Get the part of the phrase that hasn't been typed yet, preserving original case
    suggestionSuffix.value = match.slice(input.length);
  } else {
    suggestionSuffix.value = '';
  }
};

const handleKeydown = (e) => {
  if (e.key === 'Tab' && suggestionSuffix.value) {
    e.preventDefault();
    userInput.value += suggestionSuffix.value;
    suggestionSuffix.value = '';
  }
};

const useQuickAction = (action) => {
  userInput.value = action + ' ';
  suggestionSuffix.value = ''; // Clear suggestion when using quick action
  // Focus input manually if needed, but v-model binding usually suffices for next type
  const inputEl = document.querySelector('input[type="text"]');
  if (inputEl) inputEl.focus();
};

const loadClinicalCase = async () => {
  isCaseModalOpen.value = true;
  loading.value = true;
  try {
    const reqData = await getAllRequests();
    
    // Filter for AI relevant cases only (Consultation and Clinical)
    const medicalCases = reqData.filter(req => 
      req.service_type === 'consultation' || req.service_type === 'clinical'
    );

    requests.value = medicalCases.map(req => ({
      id: `req-${req.id}`,
      type: 'request',
      pet_id: req.pet_id || (req.service_data && req.service_data.pet_id), // Capture pet_id from top level or service_data
      date: req.service_data.preferredDate ? req.service_data.preferredDate.split('T')[0] : 'Pendiente',
      petName: req.pet_name || req.service_data.petName || 'Sin nombre',
      species: req.service_data.species || 'General',
      description: req.service_data.symptoms || req.service_data.description || req.service_data.notes || 'Solicitud de servicio',
      images: req.images || [],
      clinical_insights: req.service_data.clinical_insights // Capture existing insights
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

const currentPetId = ref(null); // Store selected pet ID
const selectedImage = ref(null);
const selectedImagePreview = ref(null);

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const reader = new FileReader();
  reader.onload = (e) => {
    selectedImage.value = e.target.result.split(',')[1]; // Base64 content only
    selectedImagePreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
};

const clearImage = () => {
  selectedImage.value = null;
  selectedImagePreview.value = null;
};

// Voice Recognition
const isRecording = ref(false);
let recognition = null;

const toggleVoiceRecording = () => {
  if (isRecording.value) {
    if (recognition) recognition.stop();
    isRecording.value = false;
  } else {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert('Tu navegador no soporta reconocimiento de voz.');
      return;
    }

    recognition = new SpeechRecognition();
    recognition.lang = 'es-ES';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => {
      isRecording.value = true;
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      userInput.value += (userInput.value ? ' ' : '') + transcript;
    };

    recognition.onerror = (event) => {
      console.error('Voice error:', event.error);
      isRecording.value = false;
    };

    recognition.onend = () => {
      isRecording.value = false;
    };

    recognition.start();
  }
};

const selectCase = (item) => {
  currentPetId.value = item.pet_id; // Store pet_id
  let prompt = `Paciente: ${item.petName} (${item.species})\n`;
  prompt += `Fecha: ${item.date}\n\n`;
  prompt += `Síntomas/Descripción:\n${item.description}`;

  userInput.value = prompt;
  
  // Load existing insights if available
  if (item.clinical_insights) {
    console.log('Loading existing insights:', item.clinical_insights);
    clinicalInsights.value = item.clinical_insights;
  } else {
    clinicalInsights.value = null;
  }

  closeCaseModal();
};

const formatMessage = (content) => {
  if (!content) return '';
  
  let formatted = content.replace(/!\[.*?\]\((.*?)\)/g, (match, alt, url) => {
    return `<div class="my-2"><img src="${url}" alt="${alt}" class="rounded-lg max-w-full sm:max-w-xs h-auto shadow-sm border border-slate-200 object-cover" /></div>`;
  });

  formatted = formatted.replace(/^###\s+(.*)$/gm, '<div class="font-bold text-slate-800 mt-3 mb-1 text-sm uppercase tracking-wide">$1</div>');
  formatted = formatted.replace(/^##\s+(.*)$/gm, '<div class="font-bold text-slate-800 mt-2 mb-1">$1</div>');

  formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

  formatted = formatted.replace(/^\s*-\s+(.*)$/gm, '<li class="ml-4 list-disc">$1</li>');

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

const streamResponse = async (fullText) => {
  messages.value.push({ role: 'assistant', content: '' });
  const messageIndex = messages.value.length - 1;
  
  const chunkSize = 3; // Characters per tick
  let currentIndex = 0;
  
  return new Promise((resolve) => {
    const interval = setInterval(() => {
      if (currentIndex >= fullText.length) {
        clearInterval(interval);
        resolve();
        return;
      }
      
      const chunk = fullText.slice(currentIndex, currentIndex + chunkSize);
      messages.value[messageIndex].content += chunk;
      currentIndex += chunkSize;
      scrollToBottom();
    }, 15); // Speed in ms
  });
};

const sendMessage = async () => {
  if (!userInput.value.trim() && !selectedImage.value) return;

  const content = userInput.value;
  messages.value.push({ role: 'user', content });
  
  if (selectedImagePreview.value) {
    messages.value.push({ role: 'user', content: `![Imagen adjunta](${selectedImagePreview.value})` });
  }

  userInput.value = '';
  loading.value = true;
  clinicalInsights.value = null; // Clear previous insights to show analyzing state
  await scrollToBottom();

  try {
    const payload = {
      messages: messages.value.filter(m => !m.content.startsWith('![')), 
      pet_id: currentPetId.value,
      image_data: selectedImage.value
    };

    const response = await axios.post(`${import.meta.env.VITE_API_URL}/v1/ai/chat`, payload);
    
    // Stop loading animation before streaming starts
    loading.value = false;

    // Update insights IMMEDIATELY before streaming text
    if (response.data.clinical_insights) {
      console.log('Received Clinical Insights:', response.data.clinical_insights);
      clinicalInsights.value = response.data.clinical_insights;
    } else {
      console.log('No Clinical Insights in response');
      // Optional: Set to empty object or specific state if needed, 
      // but null keeps "Analizando..." or we can add a "No insights" state.
      // For now, let's leave it null or set to empty object to remove "Analizando" spinner
      clinicalInsights.value = {}; 
    }

    if (response.data.category) {
      currentCategory.value = response.data.category;
    }
    
    // Stream the response
    await streamResponse(response.data.response);
    
    // Clear image after sending
    clearImage();

  } catch (err) {
    console.error('Error in chat:', err);
    loading.value = false;
    messages.value.push({ role: 'assistant', content: 'Lo siento, tuve un problema de conexión. Por favor intenta de nuevo.' });
  } finally {
    // loading is already false here
    await scrollToBottom();
  }
};

const generatingReport = ref(false);
const showReportModal = ref(false);
const reportContent = ref('');

const generateReport = async () => {
  generatingReport.value = true;
  try {
    const payload = {
      messages: messages.value,
      pet_id: currentPetId.value
    };
    const response = await axios.post(`${import.meta.env.VITE_API_URL}/v1/ai/report`, payload);
    reportContent.value = response.data.report;
    showReportModal.value = true;
  } catch (err) {
    console.error('Error generating report:', err);
    alert('Error al generar el reporte.');
  } finally {
    generatingReport.value = false;
  }
};



// Appointment Scheduling
const showScheduleModal = ref(false);
const appointmentData = ref({
  date: null,
  timeSlot: '',
  isUrgent: false
});
const scheduleNotes = ref('');
const takenSlots = ref([]);

watch(() => appointmentData.value.date, async (newDate) => {
  if (!newDate) {
    takenSlots.value = [];
    return;
  }
  
  try {
    const dateStr = newDate.toISOString().split('T')[0];
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/v1/appointments/all`, {
      headers: { Authorization: `Bearer ${userStore.token}` }
    });
    
    // Filter for selected date
    const dayAppointments = response.data.filter(app => app.appointment_date === dateStr && app.status !== 'cancelled');
    
    // Map times to slots
    const timeToSlot = {
      '09:00:00': 'morning',
      '08:00:00': 'morning',
      '14:00:00': 'afternoon',
      '18:00:00': 'evening'
    };
    
    takenSlots.value = dayAppointments.map(app => timeToSlot[app.appointment_time]).filter(Boolean);
    
  } catch (err) {
    console.error('Error checking availability:', err);
  }
});

const handleSchedule = (followUpData) => {
  if (!currentPetId.value) {
    addToast('Debes seleccionar un paciente primero', 'warning');
    return;
  }
  
  scheduleNotes.value = `Seguimiento sugerido por IA: ${followUpData.reason}`;
  showScheduleModal.value = true;
};

const confirmAppointment = async () => {
  if (!appointmentData.value.date || (!appointmentData.value.timeSlot && !appointmentData.value.isUrgent)) {
    addToast('Por favor selecciona fecha y hora', 'warning');
    return;
  }

  loading.value = true;
  try {
    // Map time slots to specific times
    const timeMap = {
      'morning': '09:00:00',
      'afternoon': '14:00:00',
      'evening': '18:00:00'
    };

    const payload = {
      pet_id: currentPetId.value,
      service_id: 1, // Assuming 1 is consultation/general for now
      appointment_date: appointmentData.value.date.toISOString().split('T')[0],
      appointment_time: appointmentData.value.isUrgent ? '08:00:00' : timeMap[appointmentData.value.timeSlot],
      notes: scheduleNotes.value
    };

    await axios.post(`${import.meta.env.VITE_API_URL}/v1/appointments/`, payload, {
      headers: { Authorization: `Bearer ${userStore.token}` }
    });

    addToast('Cita agendada exitosamente', 'success');
    showScheduleModal.value = false;
    
    // Reset form
    appointmentData.value = { date: null, timeSlot: '', isUrgent: false };
    scheduleNotes.value = '';

  } catch (err) {
    console.error('Error scheduling appointment:', err);
    addToast('Error al agendar la cita', 'error');
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  if (route.query.petId) {
    currentPetId.value = route.query.petId;
    const petName = route.query.petName || 'el paciente';
    messages.value.push({
      role: 'assistant',
      content: `Entendido, analicemos el caso de **${petName}**. ¿Qué síntomas presenta o qué consulta tienes sobre este paciente?`
    });

    // If requestId is present, fetch insights
    if (route.query.requestId) {
      try {
        const req = await getRequestById(route.query.requestId);
        if (req) {
          // Ensure pet_id is set if missing from query
          // Check top level or inside service_data
          const foundPetId = req.pet_id || (req.service_data && req.service_data.pet_id);
          
          if (!currentPetId.value && foundPetId) {
            currentPetId.value = foundPetId;
            console.log('Set currentPetId from request details:', currentPetId.value);
          } else if (!currentPetId.value && req.user_id && req.pet_name) {
             // Fallback: Try to find pet by name for this user
             try {
               console.log('Attempting to find pet by name:', req.pet_name, 'for user:', req.user_id);
               const userPets = await getPetsByUserId(req.user_id);
               const matchedPet = userPets.find(p => p.name.toLowerCase() === req.pet_name.toLowerCase());
               if (matchedPet) {
                 currentPetId.value = matchedPet.id;
                 console.log('Found matched pet by name:', matchedPet);
               } else {
                 console.warn('No pet found with name:', req.pet_name);
               }
             } catch (e) {
               console.error('Error fetching user pets for fallback:', e);
             }
          } else if (!currentPetId.value) {
             console.warn('Could not find pet_id in request details');
          }

          if (req.service_data && req.service_data.clinical_insights) {
            console.log('Loaded insights from URL requestId:', req.service_data.clinical_insights);
            clinicalInsights.value = req.service_data.clinical_insights;
          }
        }
      } catch (err) {
        console.error('Error loading request details:', err);
      }
    }
  }
});
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