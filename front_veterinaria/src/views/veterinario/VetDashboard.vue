<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import { CheckCircleIcon, XCircleIcon, ClockIcon } from '@heroicons/vue/24/outline';

const appointments = ref([]);
const loading = ref(true);
const error = ref(null);
const userStore = useUserStore();

const fetchPendingAppointments = async () => {
  loading.value = true;
  try {
    const response = await axios.get('http://localhost:8000/api/appointments/pending', {
      headers: { Authorization: `Bearer ${userStore.token}` }
    });
    appointments.value = response.data;
  } catch (err) {
    console.error('Error fetching appointments:', err);
    error.value = 'No se pudieron cargar las citas pendientes.';
  } finally {
    loading.value = false;
  }
};

const updateStatus = async (id, status) => {
  try {
    await axios.patch(`http://localhost:8000/api/appointments/${id}/status`, 
      { status },
      { headers: { Authorization: `Bearer ${userStore.token}` } }
    );
    // Remove from list or update local state
    appointments.value = appointments.value.filter(app => app.id !== id);
  } catch (err) {
    console.error('Error updating status:', err);
    alert('Error al actualizar el estado de la cita');
  }
};

onMounted(() => {
  fetchPendingAppointments();
});
</script>

<template>
  <div>
    <div v-if="loading" class="flex justify-center py-12">
      <LoadingSpinner />
    </div>

    <div v-else-if="error" class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-6" role="alert">
      <p>{{ error }}</p>
    </div>

    <div v-else>
      <div v-if="appointments.length === 0" class="bg-white rounded-lg shadow-md p-8 text-center">
        <ClockIcon class="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900">No hay citas pendientes</h3>
        <p class="text-gray-500 mt-2">Todas las solicitudes han sido procesadas.</p>
      </div>

      <div v-else class="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <div v-for="app in appointments" :key="app.id" class="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200 hover:shadow-lg transition-shadow">
          <div class="p-5">
            <div class="flex justify-between items-start mb-4">
              <div>
                <h3 class="text-lg font-bold text-gray-900">Cita #{{ app.id }}</h3>
                <p class="text-sm text-gray-500">{{ app.appointment_date }} - {{ app.appointment_time }}</p>
              </div>
              <span class="px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
                Pendiente
              </span>
            </div>
            
            <div class="space-y-2 mb-4">
              <p class="text-sm"><span class="font-medium text-gray-700">Cliente ID:</span> {{ app.user_id }}</p>
              <p class="text-sm"><span class="font-medium text-gray-700">Mascota ID:</span> {{ app.pet_id || 'N/A' }}</p>
              <p class="text-sm"><span class="font-medium text-gray-700">Servicio ID:</span> {{ app.service_id || 'Consulta General' }}</p>
              <div v-if="app.notes" class="mt-2 p-2 bg-gray-50 rounded text-sm text-gray-600 italic">
                "{{ app.notes }}"
              </div>
            </div>

            <div class="flex space-x-3 mt-4 pt-4 border-t border-gray-100">
              <button 
                @click="updateStatus(app.id, 'confirmed')"
                class="flex-1 flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
              >
                <CheckCircleIcon class="h-4 w-4 mr-2" />
                Confirmar
              </button>
              <button 
                @click="updateStatus(app.id, 'cancelled')"
                class="flex-1 flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
              >
                <XCircleIcon class="h-4 w-4 mr-2" />
                Cancelar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
