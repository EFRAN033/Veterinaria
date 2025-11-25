<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import LoadingSpinner from '@/components/LoadingSpinner.vue';

const appointments = ref([]);
const loading = ref(true);
const userStore = useUserStore();
const searchTerm = ref('');

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
  return appointments.value.filter(app => 
    app.id.toString().includes(searchTerm.value) ||
    app.status.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
    (app.notes && app.notes.toLowerCase().includes(searchTerm.value.toLowerCase()))
  );
});

const getStatusClass = (status) => {
  switch(status) {
    case 'completed': return 'bg-blue-100 text-blue-800';
    case 'cancelled': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
};

onMounted(() => {
  fetchHistory();
});
</script>

<template>
  <div class="bg-white rounded-lg shadow-md overflow-hidden">
    <div class="p-6 border-b border-gray-200 flex justify-between items-center">
      <h2 class="text-lg font-medium text-gray-900">Historial de Citas</h2>
      <div class="relative">
        <input 
          v-model="searchTerm" 
          type="text" 
          placeholder="Buscar..." 
          class="pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        >
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
          </svg>
        </div>
      </div>
    </div>

    <div v-if="loading" class="p-12 flex justify-center">
      <LoadingSpinner />
    </div>

    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Hora</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cliente</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Notas</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="app in filteredAppointments" :key="app.id" class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">#{{ app.id }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ app.appointment_date }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ app.appointment_time }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">ID: {{ app.user_id }}</td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getStatusClass(app.status)">
                {{ app.status }}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 truncate max-w-xs">{{ app.notes || '-' }}</td>
          </tr>
          <tr v-if="filteredAppointments.length === 0">
            <td colspan="6" class="px-6 py-10 text-center text-gray-500">
              No se encontraron registros
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
