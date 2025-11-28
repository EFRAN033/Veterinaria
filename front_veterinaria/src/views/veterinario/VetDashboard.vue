<template>
  <div class="min-h-screen bg-white font-sans text-slate-600">
    
    <!-- Header Section -->
    <div class="border-b border-slate-100 bg-white sticky top-0 z-30">
      <div class="px-6 py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Panel Veterinario</h1>
          <p class="text-sm text-slate-500">Gestión de citas y solicitudes</p>
        </div>
        
        <div class="flex items-center gap-4">
          <!-- Stats Bar (Minimalist) -->
          <div class="hidden md:flex items-center gap-6 text-sm border-r border-slate-200 pr-6 mr-2">
            <div class="flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-amber-500"></span>
              <span class="font-medium text-slate-600">Pendientes: <span class="font-bold text-slate-900">{{ totalPendingCount }}</span></span>
            </div>
            <div class="flex items-center gap-2">
              <span class="w-2 h-2 rounded-full bg-rose-500"></span>
              <span class="font-medium text-slate-600">Urgentes: <span class="font-bold text-slate-900">{{ totalUrgentCount }}</span></span>
            </div>
            <div class="flex items-center gap-2">
              <span class="relative flex h-2 w-2">
                <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
              </span>
              <span class="font-medium text-slate-600">Sistema: <span class="font-bold text-emerald-600">En línea</span></span>
            </div>
          </div>

          <button 
            @click="fetchPendingAppointments" 
            class="flex items-center gap-2 text-xs font-bold text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-4 py-2 rounded-lg transition-colors"
            :disabled="loading"
          >
            <ArrowPathIcon class="h-4 w-4" :class="{ 'animate-spin': loading }" />
            <span>Sincronizar</span>
          </button>
        </div>
      </div>
    </div>

    <div class="p-6 max-w-[1600px] mx-auto">
      
      <!-- Service Requests Section (Imported) -->
      <div class="mb-12">
        <ServiceRequestsList />
      </div>

      <!-- Appointments Section -->
      <div>
        <div class="flex flex-col sm:flex-row justify-between items-end gap-4 mb-6 border-b border-slate-200 pb-4">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Citas Programadas</h2>
            <p class="text-sm text-slate-500 mt-1">Próximas atenciones confirmadas</p>
          </div>

          <div class="flex items-center gap-4 w-full sm:w-auto">
            <!-- Tabs -->
            <div class="flex gap-4 text-sm font-medium">
              <button 
                v-for="tab in ['Todos', 'Urgentes']" 
                :key="tab"
                @click="activeTab = tab"
                class="pb-1 border-b-2 transition-colors"
                :class="activeTab === tab ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500 hover:text-slate-700'"
              >
                {{ tab }}
              </button>
            </div>

            <!-- Search -->
            <div class="relative group">
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="Buscar..." 
                class="pl-9 pr-4 py-1.5 text-sm bg-slate-50 border-b border-slate-200 focus:border-indigo-500 focus:outline-none transition-all w-48 focus:w-64"
              />
              <MagnifyingGlassIcon class="h-4 w-4 text-slate-400 absolute left-2 top-2" />
            </div>
          </div>
        </div>

        <!-- Appointments Table -->
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-200">
                <th class="py-3 px-4">Horario</th>
                <th class="py-3 px-4">Paciente</th>
                <th class="py-3 px-4">Servicio</th>
                <th class="py-3 px-4">Notas</th>
                <th class="py-3 px-4">Estado</th>
                <th class="py-3 px-4 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr v-if="loading" class="animate-pulse">
                <td colspan="6" class="py-8 text-center text-slate-400">Cargando datos...</td>
              </tr>
              <tr v-else-if="error">
                <td colspan="6" class="py-8 text-center text-rose-500">{{ error }}</td>
              </tr>
              <tr v-else-if="filteredAppointments.length === 0">
                <td colspan="6" class="py-12 text-center text-slate-400">
                  <ClipboardDocumentCheckIcon class="h-12 w-12 mx-auto mb-2 opacity-50" />
                  No hay citas pendientes
                </td>
              </tr>
              
              <tr 
                v-for="app in filteredAppointments" 
                :key="app.id"
                class="group hover:bg-slate-50 transition-colors border-b border-slate-100 last:border-0"
              >
                <td class="py-4 px-4">
                  <div class="flex items-center gap-3">
                    <div class="text-center min-w-[3rem]">
                      <div class="text-xs font-bold text-slate-400 uppercase">{{ getDayName(app.appointment_date) }}</div>
                      <div class="text-lg font-bold text-slate-800">{{ getDayNumber(app.appointment_date) }}</div>
                    </div>
                    <div class="h-8 w-px bg-slate-200"></div>
                    <span class="font-mono font-medium text-slate-600">{{ app.appointment_time.substring(0, 5) }}</span>
                  </div>
                </td>
                
                <td class="py-4 px-4">
                  <div>
                    <p class="font-bold text-slate-800">Cliente #{{ app.user_id }}</p>
                    <div class="flex items-center gap-1 text-xs text-slate-500 mt-0.5">
                      <TagIcon class="h-3 w-3" />
                      <span>{{ app.pet_id || 'Mascota sin ID' }}</span>
                    </div>
                  </div>
                </td>

                <td class="py-4 px-4">
                  <span class="font-medium text-slate-700">{{ app.service_id || 'Consulta General' }}</span>
                </td>

                <td class="py-4 px-4 max-w-xs">
                  <p class="truncate text-slate-500 italic" :title="app.notes">{{ app.notes || '-' }}</p>
                </td>

                <td class="py-4 px-4">
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-amber-50 text-amber-600">
                    <span class="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
                    Revisión
                  </span>
                </td>

                <td class="py-4 px-4 text-right">
                  <div class="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button 
                      @click="updateStatus(app.id, 'confirmed')"
                      class="text-xs font-bold text-emerald-600 hover:text-emerald-800 hover:bg-emerald-50 px-3 py-1.5 rounded transition-colors"
                    >
                      Aprobar
                    </button>
                    <button 
                      @click="updateStatus(app.id, 'cancelled')"
                      class="text-xs font-bold text-rose-600 hover:text-rose-800 hover:bg-rose-50 px-3 py-1.5 rounded transition-colors"
                    >
                      Rechazar
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
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
  ArrowPathIcon,
  TagIcon,
  MagnifyingGlassIcon,
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
const { addToast } = useToast();

const getDayName = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('es-ES', { weekday: 'short' }).substring(0, 3);
};

const getDayNumber = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.getDate();
};

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

const totalPendingCount = computed(() => {
  return appointments.value.length + serviceRequests.value.length;
});

const totalUrgentCount = computed(() => {
  const urgentAppointments = appointments.value.filter(app => 
    app.notes && (app.notes.toLowerCase().includes('urgente') || app.notes.toLowerCase().includes('dolor'))
  ).length;
  
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
    const appointmentsResponse = await axios.get(`${import.meta.env.VITE_API_URL}/v1/appointments/pending`, {
      headers: { Authorization: `Bearer ${userStore.token}` }
    });
    appointments.value = appointmentsResponse.data;
    
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
    await axios.patch(`${import.meta.env.VITE_API_URL}/v1/appointments/${id}/status`, 
      { status },
      { headers: { Authorization: `Bearer ${userStore.token}` } }
    );
    addToast('Cita actualizada correctamente', 'success');
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