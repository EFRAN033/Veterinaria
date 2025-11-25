<template>
  <div class="min-h-screen bg-gray-50 font-sans text-gray-900">
    
    <header class="bg-white shadow-sm sticky top-0 z-10 border-b border-gray-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="bg-indigo-600 p-2 rounded-lg">
            <CalendarDaysIcon class="h-6 w-6 text-white" />
          </div>
          <h1 class="text-xl font-bold tracking-tight text-gray-900">Panel de Citas</h1>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-sm text-gray-500 bg-gray-100 px-3 py-1 rounded-full hidden sm:inline-block">
            <span class="w-2 h-2 rounded-full bg-green-500 inline-block mr-2"></span>
            Sistema Operativo
          </span>
          <button @click="fetchPendingAppointments" class="p-2 text-gray-400 hover:text-indigo-600 transition-colors" title="Recargar datos">
            <ArrowPathIcon class="h-6 w-6" :class="{ 'animate-spin': loading }" />
          </button>
        </div>
      </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-3 mb-8">
        <div class="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-100 p-5 flex items-center justify-between">
          <div>
            <p class="text-sm font-medium text-gray-500 truncate">Solicitudes Pendientes</p>
            <p class="mt-1 text-3xl font-semibold text-indigo-600">{{ appointments.length }}</p>
          </div>
          <div class="bg-indigo-50 p-3 rounded-full">
            <InboxStackIcon class="h-6 w-6 text-indigo-600" />
          </div>
        </div>
        <div class="bg-white overflow-hidden shadow-sm rounded-xl border border-gray-100 p-5 flex items-center justify-between opacity-60">
          <div>
            <p class="text-sm font-medium text-gray-500 truncate">Citas Hoy</p>
            <p class="mt-1 text-3xl font-semibold text-gray-900">-</p>
          </div>
          <div class="bg-gray-50 p-3 rounded-full">
            <ClockIcon class="h-6 w-6 text-gray-400" />
          </div>
        </div>
      </div>

      <div v-if="loading" class="bg-white rounded-xl shadow-sm p-10 flex flex-col items-center justify-center min-h-[400px]">
        <LoadingSpinner />
        <p class="mt-4 text-gray-400 text-sm animate-pulse">Sincronizando citas...</p>
      </div>

      <div v-else-if="error" class="bg-white rounded-xl shadow-sm p-6 border-l-4 border-red-500 mb-6 flex items-start gap-4">
        <ExclamationTriangleIcon class="h-6 w-6 text-red-500 shrink-0" />
        <div>
          <h3 class="text-sm font-medium text-red-800">Error de conexión</h3>
          <p class="text-sm text-red-600 mt-1">{{ error }}</p>
          <button @click="fetchPendingAppointments" class="mt-3 text-sm text-red-700 underline hover:text-red-900">Reintentar</button>
        </div>
      </div>

      <div v-else>
        <div v-if="appointments.length === 0" class="bg-white rounded-xl shadow-sm border border-gray-200 border-dashed p-12 text-center">
          <div class="mx-auto h-16 w-16 bg-green-50 rounded-full flex items-center justify-center mb-4">
            <CheckBadgeIcon class="h-10 w-10 text-green-500" />
          </div>
          <h3 class="text-lg font-medium text-gray-900">¡Estás al día!</h3>
          <p class="mt-2 text-gray-500 max-w-sm mx-auto">No hay nuevas solicitudes de citas pendientes de revisión en este momento.</p>
        </div>

        <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-100 bg-gray-50/50 flex justify-between items-center">
            <h3 class="text-base font-semibold leading-6 text-gray-900">Listado de Solicitudes</h3>
            <span class="bg-blue-100 text-blue-700 text-xs font-medium px-2.5 py-0.5 rounded-full">Acción requerida</span>
          </div>
          
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="py-4 pl-6 pr-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Paciente & Dueño</th>
                  <th scope="col" class="px-3 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Agenda</th>
                  <th scope="col" class="px-3 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Detalle Servicio</th>
                  <th scope="col" class="px-3 py-4 text-right text-xs font-medium text-gray-500 uppercase tracking-wider pr-6">Decisión</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 bg-white">
                <tr v-for="app in appointments" :key="app.id" class="group hover:bg-indigo-50/30 transition-colors duration-200">
                  
                  <td class="whitespace-nowrap py-5 pl-6 pr-3">
                    <div class="flex items-center">
                      <div class="h-10 w-10 flex-shrink-0 rounded-full bg-gradient-to-br from-purple-500 to-indigo-500 flex items-center justify-center text-white text-sm font-bold shadow-sm">
                        {{ app.user_id.toString().slice(0,2) }}
                      </div>
                      <div class="ml-4">
                        <div class="font-semibold text-gray-900">Cliente #{{ app.user_id }}</div>
                        <div class="text-gray-500 text-xs flex items-center gap-1">
                          <span class="inline-block w-1.5 h-1.5 rounded-full bg-gray-300"></span>
                          Mascota ID: <span class="font-mono text-gray-600">{{ app.pet_id || 'N/A' }}</span>
                        </div>
                      </div>
                    </div>
                  </td>

                  <td class="whitespace-nowrap px-3 py-5">
                    <div class="flex flex-col">
                      <div class="flex items-center gap-2 text-gray-900 font-medium">
                        <CalendarIcon class="h-4 w-4 text-indigo-500" />
                        {{ formatDate(app.appointment_date) }}
                      </div>
                      <div class="flex items-center gap-2 text-gray-500 text-sm mt-1 pl-6">
                        <span class="bg-gray-100 text-gray-600 px-1.5 rounded text-xs font-mono">{{ app.appointment_time }}</span>
                      </div>
                    </div>
                  </td>

                  <td class="px-3 py-5">
                    <div class="flex flex-col items-start gap-2">
                      <span class="inline-flex items-center rounded-md bg-indigo-50 px-2 py-1 text-xs font-medium text-indigo-700 ring-1 ring-inset ring-indigo-600/10">
                        {{ app.service_id || 'Consulta General' }}
                      </span>
                      <p v-if="app.notes" class="text-xs text-gray-500 italic max-w-[200px] truncate border-l-2 border-gray-200 pl-2" :title="app.notes">
                        {{ app.notes }}
                      </p>
                    </div>
                  </td>

                  <td class="relative whitespace-nowrap py-5 pl-3 pr-6 text-right">
                    <div class="flex justify-end items-center gap-3 opacity-100 sm:opacity-80 group-hover:opacity-100 transition-opacity">
                      <button 
                        @click="updateStatus(app.id, 'cancelled')"
                        class="text-xs font-medium text-gray-500 hover:text-red-600 px-3 py-1.5 rounded-md hover:bg-red-50 transition-colors"
                      >
                        Cancelar
                      </button>
                      <button 
                        @click="updateStatus(app.id, 'confirmed')"
                        class="inline-flex items-center gap-x-1.5 rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 transition-all transform hover:scale-105"
                      >
                        <CheckIcon class="-ml-0.5 h-4 w-4" aria-hidden="true" />
                        Confirmar
                      </button>
                    </div>
                  </td>

                </tr>
              </tbody>
            </table>
          </div>
          <div class="bg-gray-50 px-6 py-3 border-t border-gray-200 text-xs text-gray-500 flex justify-between items-center">
            <span>Mostrando todos los pendientes</span>
            <span>Total: {{ appointments.length }}</span>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import { 
  CheckIcon, 
  XMarkIcon, 
  CalendarIcon, 
  ClockIcon, 
  ArrowPathIcon,
  CalendarDaysIcon,
  InboxStackIcon,
  CheckBadgeIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline';

const appointments = ref([]);
const loading = ref(true);
const error = ref(null);
const userStore = useUserStore();

// Formateador de fecha más amigable (ej: "Lun, 24 Nov 2023")
const formatDate = (dateString) => {
  if (!dateString) return '';
  const options = { weekday: 'short', day: 'numeric', month: 'short', year: 'numeric' };
  // Aseguramos compatibilidad con formato YYYY-MM-DD
  const dateParts = dateString.split('-');
  const date = new Date(dateParts[0], dateParts[1] - 1, dateParts[2]); 
  return date.toLocaleDateString('es-ES', options);
};

const fetchPendingAppointments = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await axios.get('http://localhost:8000/api/appointments/pending', {
      headers: { Authorization: `Bearer ${userStore.token}` }
    });
    appointments.value = response.data;
  } catch (err) {
    console.error('Error fetching appointments:', err);
    error.value = 'No se pudo conectar con el servidor.';
  } finally {
    loading.value = false;
  }
};

const updateStatus = async (id, status) => {
  if (status === 'cancelled' && !confirm(`¿Rechazar solicitud de cita?`)) return;

  // Optimistic UI Update: Eliminamos visualmente antes de esperar al servidor para sensación de rapidez
  const originalList = [...appointments.value];
  appointments.value = appointments.value.filter(app => app.id !== id);

  try {
    await axios.patch(`http://localhost:8000/api/appointments/${id}/status`, 
      { status },
      { headers: { Authorization: `Bearer ${userStore.token}` } }
    );
  } catch (err) {
    console.error('Error updating status:', err);
    // Rollback si falla
    appointments.value = originalList;
    alert('Hubo un error al actualizar. Intente nuevamente.');
  }
};

onMounted(() => {
  fetchPendingAppointments();
});
</script>