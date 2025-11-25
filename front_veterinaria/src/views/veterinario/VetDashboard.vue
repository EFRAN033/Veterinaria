<template>
  <div class="h-full flex flex-col font-sans text-slate-600 bg-slate-50/50">
    
    <div class="mb-8 shrink-0 px-1">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4 mb-6">
        <div>
          <h2 class="text-2xl font-bold text-slate-900 tracking-tight">Panel de Control</h2>
          <p class="text-sm text-slate-500 mt-1">Resumen de operaciones diarias.</p>
        </div>
        
        <button 
          @click="fetchPendingAppointments" 
          class="group flex items-center gap-2 text-xs font-bold text-indigo-600 bg-white border border-indigo-100 hover:border-indigo-300 hover:shadow-md px-4 py-2.5 rounded-xl transition-all duration-300"
          :disabled="loading"
        >
          <ArrowPathIcon class="h-4 w-4 group-hover:rotate-180 transition-transform duration-500" :class="{ 'animate-spin': loading }" />
          <span>Sincronizar Datos</span>
        </button>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-5">
        
        <div class="bg-white p-5 rounded-2xl shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-slate-100 relative overflow-hidden group hover:-translate-y-1 transition-transform duration-300">
          <div class="flex justify-between items-start relative z-10">
            <div>
              <p class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-1">Por Revisar</p>
              <p class="text-3xl font-black text-slate-800">{{ totalPendingCount }}</p>
            </div>
            <div class="p-2.5 bg-amber-50 text-amber-600 rounded-xl group-hover:bg-amber-500 group-hover:text-white transition-colors">
              <InboxStackIcon class="h-6 w-6" />
            </div>
          </div>
          <div class="absolute -right-6 -bottom-6 w-24 h-24 bg-amber-50 rounded-full opacity-50 group-hover:scale-150 transition-transform duration-500"></div>
        </div>

        <div class="bg-white p-5 rounded-2xl shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-slate-100 relative overflow-hidden group hover:-translate-y-1 transition-transform duration-300">
          <div class="flex justify-between items-start relative z-10">
            <div>
              <p class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-1">Prioridad Alta</p>
              <p class="text-3xl font-black text-slate-800">{{ totalUrgentCount }}</p>
            </div>
            <div class="p-2.5 bg-rose-50 text-rose-600 rounded-xl group-hover:bg-rose-500 group-hover:text-white transition-colors">
              <ExclamationTriangleIcon class="h-6 w-6" />
            </div>
          </div>
          <div class="absolute -right-6 -bottom-6 w-24 h-24 bg-rose-50 rounded-full opacity-50 group-hover:scale-150 transition-transform duration-500"></div>
        </div>

        <div class="bg-white p-5 rounded-2xl shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-slate-100 relative overflow-hidden group hover:-translate-y-1 transition-transform duration-300">
          <div class="flex justify-between items-start relative z-10">
            <div>
              <p class="text-[11px] font-bold text-slate-400 uppercase tracking-widest mb-1">Estado Sistema</p>
              <div class="flex items-center gap-2 mt-1.5">
                <span class="relative flex h-3 w-3">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                </span>
                <span class="text-sm font-bold text-slate-700">En línea</span>
              </div>
            </div>
            <div class="p-2.5 bg-indigo-50 text-indigo-600 rounded-xl group-hover:bg-indigo-500 group-hover:text-white transition-colors">
              <ServerIcon class="h-6 w-6" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Service Requests Section -->
    <div class="mb-8 shrink-0">
      <ServiceRequestsList />
    </div>

    <div class="flex-1 flex flex-col min-h-0">
      
      <div class="flex flex-col sm:flex-row justify-between items-center gap-4 mb-4 px-1">
        <div class="bg-white p-1 rounded-xl border border-slate-200 shadow-sm flex">
          <button 
            v-for="tab in ['Todos', 'Urgentes']" 
            :key="tab"
            @click="activeTab = tab"
            class="px-4 py-1.5 text-[11px] font-bold uppercase tracking-wide rounded-lg transition-all duration-200"
            :class="activeTab === tab ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-500 hover:bg-slate-50'"
          >
            {{ tab }}
          </button>
        </div>

        <div class="relative w-full sm:w-64 group">
          <input 
            v-model="searchQuery"
            type="text" 
            placeholder="Buscar por cliente, mascota..." 
            class="w-full pl-10 pr-4 py-2.5 text-xs font-medium bg-white border border-slate-200 rounded-xl focus:outline-none focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 text-slate-600 shadow-sm transition-all group-hover:border-indigo-300"
          />
          <MagnifyingGlassIcon class="h-4 w-4 text-slate-400 absolute left-3.5 top-3 group-hover:text-indigo-500 transition-colors" />
        </div>
      </div>

      <div class="flex-1 bg-white rounded-t-3xl shadow-[0_-4px_20px_rgba(0,0,0,0.02)] border border-slate-200 overflow-hidden flex flex-col">
        
        <div class="grid grid-cols-12 gap-4 px-6 py-4 border-b border-slate-100 bg-slate-50/50 text-[10px] font-bold text-slate-400 uppercase tracking-wider">
          <div class="col-span-2">Horario</div>
          <div class="col-span-3">Paciente</div>
          <div class="col-span-3">Servicio</div>
          <div class="col-span-2">Estado</div>
          <div class="col-span-2 text-right">Acción</div>
        </div>

        <div v-if="loading" class="flex-1 flex flex-col items-center justify-center space-y-4">
          <LoadingSpinner />
          <p class="text-xs font-medium text-slate-400 animate-pulse">Conectando con servidor...</p>
        </div>

        <div v-else-if="error" class="flex-1 flex flex-col items-center justify-center p-8">
          <div class="bg-rose-50 p-4 rounded-full mb-4">
            <ExclamationTriangleIcon class="h-8 w-8 text-rose-500" />
          </div>
          <h3 class="text-slate-800 font-bold text-lg">Algo salió mal</h3>
          <p class="text-slate-500 text-sm mt-1 mb-4">{{ error }}</p>
          <button @click="fetchPendingAppointments" class="text-xs font-bold text-indigo-600 hover:text-indigo-800 underline">Reintentar conexión</button>
        </div>

        <div v-else class="flex-1 overflow-y-auto custom-scrollbar p-2">
          
          <div v-if="filteredAppointments.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400 opacity-60">
            <ClipboardDocumentCheckIcon class="h-16 w-16 mb-4 text-slate-200" />
            <p class="text-sm font-medium">No hay solicitudes pendientes</p>
          </div>

          <div 
            v-for="app in filteredAppointments" 
            :key="app.id" 
            class="grid grid-cols-12 gap-4 items-center px-4 py-3 mb-2 rounded-xl hover:bg-slate-50 transition-all duration-200 border border-transparent hover:border-slate-100 group"
          >
            <div class="col-span-2 flex items-center gap-3">
              <div class="w-10 h-10 rounded-lg bg-indigo-50 text-indigo-700 flex flex-col items-center justify-center font-bold border border-indigo-100/50">
                <span class="text-[9px] uppercase leading-none mt-0.5">{{ getDayName(app.appointment_date) }}</span>
                <span class="text-sm leading-none">{{ getDayNumber(app.appointment_date) }}</span>
              </div>
              <span class="text-xs font-bold text-slate-600 font-mono">{{ app.appointment_time.substring(0, 5) }}</span>
            </div>

            <div class="col-span-3">
              <p class="text-sm font-bold text-slate-700 truncate">Cliente #{{ app.user_id }}</p>
              <div class="flex items-center gap-1 text-xs text-slate-500 mt-0.5">
                <TagIcon class="h-3 w-3" />
                <span class="truncate font-medium">{{ app.pet_id || 'Mascota sin ID' }}</span>
              </div>
            </div>

            <div class="col-span-3">
              <div class="flex flex-col items-start">
                <span class="text-xs font-bold text-slate-700">{{ app.service_id || 'Consulta General' }}</span>
                <p v-if="app.notes" class="text-[10px] text-slate-400 italic truncate w-full max-w-[150px]" :title="app.notes">
                  {{ app.notes }}
                </p>
              </div>
            </div>

            <div class="col-span-2">
              <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wide bg-amber-50 text-amber-600 border border-amber-100">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                Revisión
              </span>
            </div>

            <div class="col-span-2 flex justify-end gap-2 opacity-100 sm:opacity-30 group-hover:opacity-100 transition-all duration-200">
              <button 
                @click="updateStatus(app.id, 'cancelled')"
                class="p-2 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
                title="Rechazar"
              >
                <XMarkIcon class="h-5 w-5" />
              </button>
              <button 
                @click="updateStatus(app.id, 'confirmed')"
                class="p-2 rounded-lg text-slate-400 hover:text-emerald-600 hover:bg-emerald-50 transition-colors"
                title="Aprobar"
              >
                <CheckIcon class="h-5 w-5" />
              </button>
            </div>
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
import { useToast } from '@/composables/useToast';
import { useServiceRequests } from '@/composables/useServiceRequests';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import ServiceRequestsList from '@/components/ServiceRequestsList.vue';
import { 
  CheckIcon, 
  XMarkIcon, 
  ArrowPathIcon,
  InboxStackIcon,
  ExclamationTriangleIcon,
  UserIcon,
  TagIcon,
  MagnifyingGlassIcon,
  ServerIcon,
  ClipboardDocumentCheckIcon
} from '@heroicons/vue/24/outline';

const appointments = ref([]);
const serviceRequests = ref([]);
const loading = ref(true);
const error = ref(null);
const searchQuery = ref('');
const activeTab = ref('Todos');
const userStore = useUserStore();
const { getAllRequests } = useServiceRequests();

// Helpers para fechas
const getDayName = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('es-ES', { weekday: 'short' }).substring(0, 3);
};

const getDayNumber = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.getDate();
};

// Lógica de Filtrado
const filteredAppointments = computed(() => {
  let list = appointments.value;

  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(app => 
      app.user_id.toString().includes(q) ||
      (app.pet_id && app.pet_id.toString().includes(q)) ||
      (app.notes && app.notes.toLowerCase().includes(q))
    );
  }

  if (activeTab.value === 'Urgentes') {
    const today = new Date().toISOString().split('T')[0];
    list = list.filter(app => 
      app.appointment_date === today || 
      (app.notes && app.notes.toLowerCase().includes('urgente'))
    );
  }

  return list;
});

// Contador total de items por revisar (citas + solicitudes pendientes)
const totalPendingCount = computed(() => {
  return appointments.value.length + serviceRequests.value.length;
});

// Contador total de items urgentes/prioridad alta
const totalUrgentCount = computed(() => {
  // Citas urgentes (basado en notas)
  const urgentAppointments = appointments.value.filter(app => 
    app.notes && (app.notes.toLowerCase().includes('urgente') || app.notes.toLowerCase().includes('dolor'))
  ).length;
  
  // Solicitudes de servicio con urgencia alta
  const urgentRequests = serviceRequests.value.filter(req => 
    (req.service_data && req.service_data.urgency === 'alta') ||
    (req.service_data && req.service_data.isUrgent === true)
  ).length;
  
  return urgentAppointments + urgentRequests;
});

const fetchPendingAppointments = async () => {
  loading.value = true;
  error.value = null;
  try {
    // Fetch appointments
    const appointmentsResponse = await axios.get(`${import.meta.env.VITE_API_URL}/appointments/pending`, {
      headers: { Authorization: `Bearer ${userStore.token}` }
    });
    appointments.value = appointmentsResponse.data;
    
    // Fetch pending service requests
    const requestsData = await getAllRequests({ status: 'pending' });
    serviceRequests.value = requestsData;
  } catch (err) {
    console.error('Error fetching data:', err);
    error.value = 'No se pudieron cargar las solicitudes.';
  } finally {
    loading.value = false;
  }
};

const updateStatus = async (id, status) => {
  if (status === 'cancelled' && !confirm(`¿Rechazar la solicitud #${id}?`)) return;

  const originalList = [...appointments.value];
  appointments.value = appointments.value.filter(app => app.id !== id);

  try {
    await axios.patch(`${import.meta.env.VITE_API_URL}/appointments/${id}/status`, 
      { status },
      { headers: { Authorization: `Bearer ${userStore.token}` } }
    );
  } catch (err) {
    console.error('Error updating status:', err);
    appointments.value = originalList;
    addToast('Error de conexión.', 'error');
  }
};

onMounted(() => {
  fetchPendingAppointments();
});
</script>

<style scoped>
/* Scrollbar premium y suave */
.custom-scrollbar::-webkit-scrollbar {
  width: 5px;
  height: 5px;
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