<template>
  <div class="h-full flex flex-col font-sans text-slate-600 bg-slate-50/50">
    
    <div class="mb-6 shrink-0 px-1">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        
        <div>
          <h2 class="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <ClipboardDocumentListIcon class="h-7 w-7 text-indigo-600" />
            Historial Clínico
          </h2>
          <p class="text-sm text-slate-500 mt-1">Registro histórico de atenciones y cancelaciones.</p>
        </div>

        <div class="flex items-center gap-3 bg-white p-1.5 rounded-xl border border-slate-200 shadow-sm">
          <div class="relative group">
            <input 
              v-model="searchTerm" 
              type="text" 
              placeholder="Buscar paciente, ID o nota..." 
              class="pl-9 pr-4 py-2 text-xs font-medium bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/10 text-slate-600 w-64 transition-all group-hover:bg-white"
            >
            <MagnifyingGlassIcon class="h-4 w-4 text-slate-400 absolute left-3 top-2.5 group-hover:text-indigo-500 transition-colors" />
          </div>
          
          <div class="px-3 py-2 bg-slate-100 rounded-lg border border-slate-200 flex flex-col items-center justify-center min-w-[60px]">
            <span class="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Total</span>
            <span class="text-xs font-bold text-slate-700">{{ filteredAppointments.length }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="flex-1 bg-white rounded-t-3xl shadow-[0_-4px_20px_rgba(0,0,0,0.02)] border border-slate-200 overflow-hidden flex flex-col min-h-0">
      
      <div class="grid grid-cols-12 gap-4 px-6 py-4 border-b border-slate-100 bg-slate-50/50 text-[10px] font-bold text-slate-400 uppercase tracking-wider shrink-0">
        <div class="col-span-2">Fecha / Hora</div>
        <div class="col-span-3">Paciente</div>
        <div class="col-span-2">Estado</div>
        <div class="col-span-4">Diagnóstico / Notas</div>
        <div class="col-span-1 text-right">ID</div>
      </div>

      <div v-if="loading" class="flex-1 flex flex-col items-center justify-center space-y-3">
        <LoadingSpinner />
        <p class="text-xs font-medium text-slate-400 animate-pulse">Cargando expediente...</p>
      </div>

      <div v-else class="flex-1 overflow-y-auto custom-scrollbar p-2">
        
        <div v-if="filteredAppointments.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400 opacity-60">
          <ArchiveBoxXMarkIcon class="h-16 w-16 mb-4 text-slate-200" />
          <p class="text-sm font-medium">No se encontraron registros</p>
          <p class="text-xs mt-1">Intenta con otro término de búsqueda.</p>
        </div>

        <div 
          v-for="app in filteredAppointments" 
          :key="app.id" 
          class="group grid grid-cols-12 gap-4 items-center px-4 py-3 mb-2 rounded-xl hover:bg-slate-50 transition-all duration-200 border border-transparent hover:border-slate-100 relative overflow-hidden"
        >
          <div class="absolute left-0 top-2 bottom-2 w-1 rounded-r-full" :class="getStatusBorder(app.status)"></div>

          <div class="col-span-2 pl-3">
            <div class="flex items-center gap-3">
              <div class="flex flex-col items-center justify-center w-10 h-10 rounded-lg border bg-white shadow-sm" :class="getDateBoxColor(app.status)">
                <span class="text-[9px] uppercase font-bold opacity-60">{{ getDayName(app.appointment_date) }}</span>
                <span class="text-sm font-black leading-none">{{ getDayNumber(app.appointment_date) }}</span>
              </div>
              <div class="flex flex-col">
                <span class="text-[10px] uppercase font-bold text-slate-400">{{ getMonthYear(app.appointment_date) }}</span>
                <span class="text-xs font-mono font-medium text-slate-600">{{ app.appointment_time }}</span>
              </div>
            </div>
          </div>

          <div class="col-span-3">
            <div class="flex items-center gap-2 mb-1">
              <UserIcon class="h-3.5 w-3.5 text-slate-400" />
              <span class="text-xs font-bold text-slate-700">Cliente {{ app.user_id }}</span>
            </div>
            <div class="flex items-center gap-2">
              <TagIcon class="h-3.5 w-3.5 text-slate-400" />
              <span class="text-xs text-slate-500">Mascota ID: {{ app.pet_id || 'N/A' }}</span>
            </div>
          </div>

          <div class="col-span-2">
            <span 
              class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide border"
              :class="getStatusBadge(app.status)"
            >
              <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDot(app.status)"></span>
              {{ getStatusLabel(app.status) }}
            </span>
          </div>

          <div class="col-span-4">
            <div v-if="app.notes" class="flex items-start gap-2 group-hover:bg-white p-1.5 rounded-lg transition-colors">
              <DocumentTextIcon class="h-4 w-4 text-slate-400 shrink-0 mt-0.5" />
              <p class="text-xs text-slate-600 leading-snug line-clamp-2 italic">
                {{ app.notes }}
              </p>
            </div>
            <span v-else class="text-[10px] text-slate-300 uppercase font-bold pl-2">- Sin notas -</span>
          </div>

          <div class="col-span-1 text-right">
            <span class="text-[10px] font-mono text-slate-300 font-medium">#{{ app.id }}</span>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import { 
  MagnifyingGlassIcon, 
  ClipboardDocumentListIcon,
  UserIcon,
  TagIcon,
  DocumentTextIcon,
  ArchiveBoxXMarkIcon
} from '@heroicons/vue/24/outline';

const appointments = ref([]);
const loading = ref(true);
const userStore = useUserStore();
const searchTerm = ref('');

// --- HELPERS DE FECHA ---
const getDayName = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('es-ES', { weekday: 'short' }).substring(0, 3);
};
const getDayNumber = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.getDate();
};
const getMonthYear = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('es-ES', { month: 'short', year: '2-digit' });
};

// --- HELPERS DE ESTILO ---
const getStatusBorder = (status) => {
  if (status === 'completed') return 'bg-blue-500';
  if (status === 'cancelled') return 'bg-rose-500';
  return 'bg-slate-300';
};

const getDateBoxColor = (status) => {
  if (status === 'completed') return 'border-blue-200 text-blue-700';
  if (status === 'cancelled') return 'border-rose-200 text-rose-700 opacity-75';
  return 'border-slate-200 text-slate-500';
};

const getStatusBadge = (status) => {
  if (status === 'completed') return 'bg-blue-50 text-blue-700 border-blue-100';
  if (status === 'cancelled') return 'bg-rose-50 text-rose-700 border-rose-100';
  return 'bg-slate-100 text-slate-600 border-slate-200';
};

const getStatusDot = (status) => {
  if (status === 'completed') return 'bg-blue-500';
  if (status === 'cancelled') return 'bg-rose-500';
  return 'bg-slate-400';
};

const getStatusLabel = (status) => {
  if (status === 'completed') return 'Completada';
  if (status === 'cancelled') return 'Cancelada';
  return status;
};

// --- LÓGICA ---
const fetchHistory = async () => {
  loading.value = true;
  try {
    const response = await axios.get('http://localhost:8000/api/appointments/history', {
      headers: { Authorization: `Bearer ${userStore.token}` }
    });
    appointments.value = response.data;
  } catch (err) {
    console.error('Error fetching history:', err);
  } finally {
    loading.value = false;
  }
};

const filteredAppointments = computed(() => {
  const term = searchTerm.value.toLowerCase();
  return appointments.value.filter(app => 
    app.id.toString().includes(term) ||
    app.status.toLowerCase().includes(term) ||
    app.user_id.toString().includes(term) || // Búsqueda por cliente
    (app.notes && app.notes.toLowerCase().includes(term))
  );
});

onMounted(() => {
  fetchHistory();
});
</script>

<style scoped>
/* Scrollbar premium */
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
</style>