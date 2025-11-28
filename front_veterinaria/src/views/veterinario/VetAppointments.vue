<template>
  <div class="min-h-screen bg-slate-50 font-sans text-slate-600">
    
    <!-- Header Section -->
    <div class="bg-white border-b border-slate-200 sticky top-0 z-30">
      <div class="px-6 py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <CalendarDaysIcon class="h-7 w-7 text-indigo-600" />
            Gestión de Citas
          </h1>
          <p class="text-sm text-slate-500">Administración completa de la agenda veterinaria</p>
        </div>
        
        <div class="flex items-center gap-3">
          <button 
            @click="fetchAppointments" 
            class="flex items-center gap-2 text-xs font-bold text-indigo-600 hover:text-indigo-800 bg-indigo-50 hover:bg-indigo-100 px-4 py-2 rounded-lg transition-colors"
            :disabled="loading"
          >
            <ArrowPathIcon class="h-4 w-4" :class="{ 'animate-spin': loading }" />
            <span>Actualizar</span>
          </button>
        </div>
      </div>
    </div>

    <div class="p-6 max-w-[1600px] mx-auto">
      
      <!-- Filters & Controls -->
      <div class="bg-white p-4 rounded-xl shadow-sm border border-slate-200 mb-6">
        <div class="flex flex-col md:flex-row gap-4 justify-between items-center">
          
          <!-- Status Filters -->
          <div class="flex gap-2 overflow-x-auto w-full md:w-auto pb-2 md:pb-0">
            <button 
              v-for="filter in filters" 
              :key="filter.id"
              @click="activeFilter = filter.id"
              class="px-4 py-2 rounded-lg text-sm font-bold transition-all whitespace-nowrap flex items-center gap-2"
              :class="activeFilter === filter.id 
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-200' 
                : 'bg-slate-50 text-slate-600 hover:bg-slate-100'"
            >
              <component :is="filter.icon" class="h-4 w-4" />
              {{ filter.label }}
              <span class="ml-1 text-xs opacity-80 bg-white/20 px-1.5 rounded-full">{{ getCount(filter.id) }}</span>
            </button>
          </div>

          <!-- Search & Date -->
          <div class="flex gap-3 w-full md:w-auto">
            <div class="relative group flex-1 md:w-64">
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="Buscar paciente, cliente..." 
                class="w-full pl-10 pr-4 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none transition-all"
              />
              <MagnifyingGlassIcon class="h-5 w-5 text-slate-400 absolute left-3 top-2" />
            </div>
            
            <input 
              v-model="dateFilter"
              type="date"
              class="px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-lg focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 focus:outline-none text-slate-600"
            />
          </div>
        </div>
      </div>

      <!-- Appointments Table -->
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-200 bg-slate-50/50">
                <th class="py-4 px-6">Fecha y Hora</th>
                <th class="py-4 px-6">Paciente</th>
                <th class="py-4 px-6">Servicio</th>
                <th class="py-4 px-6">Notas</th>
                <th class="py-4 px-6">Estado</th>
                <th class="py-4 px-6 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody class="text-sm">
              <tr v-if="loading" class="animate-pulse">
                <td colspan="6" class="py-12 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-2">
                    <ArrowPathIcon class="h-8 w-8 animate-spin text-indigo-300" />
                    <span>Cargando agenda...</span>
                  </div>
                </td>
              </tr>
              
              <tr v-else-if="filteredAppointments.length === 0">
                <td colspan="6" class="py-16 text-center text-slate-400">
                  <div class="flex flex-col items-center gap-3 opacity-60">
                    <InboxIcon class="h-12 w-12" />
                    <p class="font-medium">No se encontraron citas con los filtros actuales</p>
                    <button @click="clearFilters" class="text-indigo-600 hover:underline text-xs">Limpiar filtros</button>
                  </div>
                </td>
              </tr>
              
              <tr 
                v-for="app in filteredAppointments" 
                :key="app.id"
                class="group hover:bg-slate-50 transition-colors border-b border-slate-100 last:border-0"
              >
                <td class="py-4 px-6">
                  <div class="flex items-center gap-3">
                    <div class="text-center min-w-[3rem] p-1 rounded-lg bg-slate-100 border border-slate-200">
                      <div class="text-[10px] font-bold text-slate-500 uppercase">{{ getDayName(app.appointment_date) }}</div>
                      <div class="text-xl font-bold text-slate-800 leading-none mt-0.5">{{ getDayNumber(app.appointment_date) }}</div>
                    </div>
                    <div>
                      <p class="font-bold text-slate-700">{{ app.appointment_time.substring(0, 5) }}</p>
                      <p class="text-xs text-slate-400">{{ getMonthName(app.appointment_date) }}</p>
                    </div>
                  </div>
                </td>
                
                <td class="py-4 px-6">
                  <div>
                    <p class="font-bold text-slate-800 flex items-center gap-2">
                      {{ app.pet_name || 'Mascota #' + app.pet_id }}
                      <span v-if="app.pet_id" class="text-[10px] font-normal text-slate-400 bg-slate-100 px-1.5 rounded-full">ID: {{ app.pet_id }}</span>
                    </p>
                    <div class="flex items-center gap-1 text-xs text-slate-500 mt-0.5">
                      <UserIcon class="h-3 w-3" />
                      <span>Cliente #{{ app.user_id }}</span>
                    </div>
                  </div>
                </td>

                <td class="py-4 px-6">
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-indigo-50 text-indigo-700 border border-indigo-100">
                    {{ app.service_id || 'Consulta General' }}
                  </span>
                </td>

                <td class="py-4 px-6 max-w-xs">
                  <p v-if="app.notes" class="truncate text-slate-600 italic text-xs bg-yellow-50/50 p-2 rounded border border-yellow-100/50" :title="app.notes">
                    "{{ app.notes }}"
                  </p>
                  <span v-else class="text-slate-300 text-xs">-</span>
                </td>

                <td class="py-4 px-6">
                  <span 
                    class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold border"
                    :class="getStatusClass(app.status)"
                  >
                    <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDotClass(app.status)"></span>
                    {{ getStatusLabel(app.status) }}
                  </span>
                </td>

                <td class="py-4 px-6 text-right">
                  <div class="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button 
                      v-if="app.status === 'pending'"
                      @click="updateStatus(app.id, 'confirmed')"
                      class="p-1.5 text-emerald-600 hover:bg-emerald-50 rounded-lg transition-colors"
                      title="Confirmar"
                    >
                      <CheckIcon class="h-5 w-5" />
                    </button>
                    
                    <button 
                      v-if="app.status !== 'cancelled'"
                      @click="updateStatus(app.id, 'cancelled')"
                      class="p-1.5 text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                      title="Cancelar"
                    >
                      <XMarkIcon class="h-5 w-5" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination (Simple) -->
        <div class="px-6 py-4 border-t border-slate-200 bg-slate-50 flex justify-between items-center text-xs text-slate-500">
          <span>Mostrando {{ filteredAppointments.length }} citas</span>
          <!-- Future: Add real pagination controls -->
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
import { 
  CalendarDaysIcon, 
  ArrowPathIcon, 
  MagnifyingGlassIcon,
  InboxIcon,
  UserIcon,
  CheckIcon,
  XMarkIcon,
  FunnelIcon,
  CheckBadgeIcon,
  ExclamationCircleIcon
} from '@heroicons/vue/24/outline';

const appointments = ref([]);
const loading = ref(true);
const searchQuery = ref('');
const activeFilter = ref('all');
const dateFilter = ref('');
const userStore = useUserStore();
const { addToast } = useToast();

const filters = [
  { id: 'all', label: 'Todas', icon: FunnelIcon },
  { id: 'pending', label: 'Pendientes', icon: ExclamationCircleIcon },
  { id: 'confirmed', label: 'Confirmadas', icon: CheckBadgeIcon },
  { id: 'cancelled', label: 'Canceladas', icon: XMarkIcon },
];

const getCount = (status) => {
  if (status === 'all') return appointments.value.length;
  return appointments.value.filter(a => a.status === status).length;
};

const getDayName = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('es-ES', { weekday: 'short' }).substring(0, 3);
};

const getDayNumber = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.getDate();
};

const getMonthName = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('es-ES', { month: 'long' });
};

const getStatusLabel = (status) => {
  const labels = {
    pending: 'Pendiente',
    confirmed: 'Confirmada',
    cancelled: 'Cancelada'
  };
  return labels[status] || status;
};

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-amber-50 text-amber-700 border-amber-100',
    confirmed: 'bg-emerald-50 text-emerald-700 border-emerald-100',
    cancelled: 'bg-rose-50 text-rose-700 border-rose-100'
  };
  return classes[status] || 'bg-slate-50 text-slate-700';
};

const getStatusDotClass = (status) => {
  const classes = {
    pending: 'bg-amber-500',
    confirmed: 'bg-emerald-500',
    cancelled: 'bg-rose-500'
  };
  return classes[status] || 'bg-slate-500';
};

const filteredAppointments = computed(() => {
  let list = appointments.value;

  // Status Filter
  if (activeFilter.value !== 'all') {
    list = list.filter(app => app.status === activeFilter.value);
  }

  // Date Filter
  if (dateFilter.value) {
    list = list.filter(app => app.appointment_date === dateFilter.value);
  }

  // Search Filter
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(app => 
      app.user_id.toString().includes(q) ||
      (app.pet_id && app.pet_id.toString().includes(q)) ||
      (app.notes && app.notes.toLowerCase().includes(q)) ||
      (app.pet_name && app.pet_name.toLowerCase().includes(q))
    );
  }

  // Sort by date desc (newest first)
  return list.sort((a, b) => {
    const dateA = new Date(`${a.appointment_date}T${a.appointment_time}`);
    const dateB = new Date(`${b.appointment_date}T${b.appointment_time}`);
    return dateB - dateA;
  });
});

const clearFilters = () => {
  activeFilter.value = 'all';
  searchQuery.value = '';
  dateFilter.value = '';
};

const fetchAppointments = async () => {
  loading.value = true;
  try {
    const response = await axios.get(`${import.meta.env.VITE_API_URL}/v1/appointments/all`, {
      headers: { Authorization: `Bearer ${userStore.token}` }
    });
    appointments.value = response.data;
  } catch (err) {
    console.error('Error fetching appointments:', err);
    addToast('Error al cargar las citas', 'error');
  } finally {
    loading.value = false;
  }
};

const updateStatus = async (id, status) => {
  if (status === 'cancelled' && !confirm(`¿Estás seguro de cancelar la cita #${id}?`)) return;

  try {
    await axios.patch(`${import.meta.env.VITE_API_URL}/v1/appointments/${id}/status`, 
      { status },
      { headers: { Authorization: `Bearer ${userStore.token}` } }
    );
    
    // Update local state
    const appIndex = appointments.value.findIndex(a => a.id === id);
    if (appIndex !== -1) {
      appointments.value[appIndex].status = status;
    }
    
    addToast(`Cita ${status === 'confirmed' ? 'confirmada' : 'cancelada'} correctamente`, 'success');
  } catch (err) {
    console.error('Error updating status:', err);
    addToast('Error al actualizar el estado', 'error');
  }
};

onMounted(() => {
  fetchAppointments();
});
</script>
