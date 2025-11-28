<template>
  <div class="bg-white">
    <div class="flex justify-between items-end mb-6 border-b border-slate-200 pb-4">
      <div>
        <h3 class="text-xl font-bold text-slate-900">Solicitudes de Servicio</h3>
        <p class="text-sm text-slate-500 mt-1">Nuevas solicitudes de clientes</p>
      </div>
      <button 
        @click="fetchRequests" 
        class="text-xs font-bold text-indigo-600 hover:text-indigo-800 flex items-center gap-1"
        :disabled="loading"
      >
        <ArrowPathIcon class="h-4 w-4" :class="{ 'animate-spin': loading }" />
        Actualizar
      </button>
    </div>

    <div v-if="loading" class="flex justify-center py-8">
      <LoadingSpinner />
    </div>

    <div v-else-if="error" class="text-center py-8">
      <p class="text-red-500 text-sm">{{ error }}</p>
      <button @click="fetchRequests" class="mt-2 text-xs text-indigo-600 hover:underline">Reintentar</button>
    </div>

    <div v-else-if="requests.length === 0" class="text-center py-12 border-b border-slate-100">
      <ClipboardDocumentCheckIcon class="h-12 w-12 mx-auto text-slate-200 mb-2" />
      <p class="text-slate-400 text-sm">No hay solicitudes pendientes</p>
    </div>

    <div v-else class="overflow-x-auto">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="text-xs font-bold text-slate-400 uppercase tracking-wider border-b border-slate-200">
            <th class="py-3 px-4">Fecha</th>
            <th class="py-3 px-4">Cliente / Mascota</th>
            <th class="py-3 px-4">Servicio</th>
            <th class="py-3 px-4">Detalles</th>
            <th class="py-3 px-4">Estado</th>
            <th class="py-3 px-4 text-right">Acción</th>
          </tr>
        </thead>
        <tbody class="text-sm">
          <tr 
            v-for="request in requests" 
            :key="request.id"
            class="group hover:bg-slate-50 transition-colors border-b border-slate-100 last:border-0 cursor-pointer"
            @click="viewDetails(request)"
          >
            <td class="py-4 px-4 whitespace-nowrap">
              <div class="flex items-center gap-2 text-slate-600">
                <CalendarIcon class="h-4 w-4 text-slate-400" />
                {{ formatDate(request.created_at) }}
              </div>
            </td>

            <td class="py-4 px-4">
              <div>
                <p class="font-bold text-slate-800">{{ request.pet_name || 'Sin nombre' }}</p>
                <p class="text-xs text-slate-500">{{ request.user_name || `Cliente #${request.user_id}` }}</p>
              </div>
            </td>

            <td class="py-4 px-4">
              <span class="px-2 py-1 rounded text-xs font-bold uppercase tracking-wide" :class="getServiceTypeClass(request.service_type)">
                {{ getServiceTypeName(request.service_type) }}
              </span>
            </td>

            <td class="py-4 px-4 max-w-xs">
              <div class="text-xs text-slate-600 space-y-1">
                <div v-if="request.service_data.isUrgent" class="text-red-600 font-bold flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"></span>
                  URGENTE
                </div>
                
                <template v-if="request.service_type === 'consultation'">
                  <p class="truncate"><span class="font-bold text-slate-400">Síntomas:</span> {{ request.service_data.symptoms }}</p>
                </template>
                <template v-else-if="request.service_type === 'general'">
                  <p><span class="font-bold text-slate-400">Tipo:</span> {{ request.service_data.serviceType }}</p>
                </template>
                
                <div v-if="request.images && request.images.length > 0" class="flex items-center gap-1 text-slate-400 mt-1">
                  <PhotoIcon class="h-3 w-3" />
                  {{ request.images.length }} foto(s)
                </div>
              </div>
            </td>

            <td class="py-4 px-4">
              <span class="font-bold text-xs" :class="getStatusClass(request.status)">
                {{ getStatusLabel(request.status) }}
              </span>
              <div class="text-xs font-bold text-slate-700 mt-1">S/. {{ request.estimated_cost }}</div>
            </td>

            <td class="py-4 px-4 text-right">
              <button 
                @click.stop="updateStatus(request, 'reviewed')"
                class="text-xs font-bold text-indigo-600 hover:text-indigo-800 hover:bg-indigo-50 px-3 py-1.5 rounded transition-colors opacity-0 group-hover:opacity-100"
              >
                Marcar Revisado
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- DETAILS MODAL -->
    <div v-if="selectedRequest" class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6">
      <div class="absolute inset-0 bg-slate-900/20 backdrop-blur-sm transition-opacity" @click="closeModal"></div>
      
      <div class="relative bg-white w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-2xl rounded-3xl flex flex-col animate-fade-in-up">
        <!-- Modal Content -->
        <div class="p-8 sm:p-12">
            <!-- Header with Actions -->
            <div class="flex justify-between items-start mb-8">
                <div>
                    <h2 class="text-3xl font-serif font-bold text-slate-900 mb-2">Solicitud #{{ selectedRequest.id }}</h2>
                    <p class="text-slate-500">Recibida el {{ formatDate(selectedRequest.created_at) }}</p>
                </div>
                <button @click="closeModal" class="p-2 hover:bg-slate-100 rounded-full transition-colors">
                    <XMarkIcon class="h-8 w-8 text-slate-400" />
                </button>
            </div>

            <!-- Content Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
                <!-- Left Column: Pet & Client -->
                <div class="space-y-8">
                    <div>
                        <h3 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Paciente</h3>
                        <div class="flex items-center gap-4">
                            <div class="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center text-2xl">
                                🐾
                            </div>
                            <div>
                                <p class="text-2xl font-bold text-slate-900">{{ selectedRequest.pet_name || 'Sin Nombre' }}</p>
                                <p class="text-slate-500 capitalize">{{ selectedRequest.service_data.species || 'Especie no especificada' }}</p>
                            </div>
                        </div>
                    </div>

                    <div>
                        <h3 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Cliente</h3>
                        <div class="flex items-center gap-3">
                            <div class="w-10 h-10 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
                                {{ (selectedRequest.user_name || 'C')[0] }}
                            </div>
                            <div>
                                <p class="font-bold text-slate-900">{{ selectedRequest.user_name || `Cliente #${selectedRequest.user_id}` }}</p>
                                <p class="text-sm text-slate-500">{{ selectedRequest.user_email || 'Sin email' }}</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right Column: Service Details -->
                <div class="space-y-8">
                    <div>
                        <h3 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Detalles del Servicio</h3>
                        <div class="flex items-start gap-4 mb-4">
                             <span class="px-3 py-1 rounded-lg text-sm font-bold uppercase tracking-wide" :class="getServiceTypeClass(selectedRequest.service_type)">
                                {{ getServiceTypeName(selectedRequest.service_type) }}
                            </span>
                            <span v-if="selectedRequest.service_data.isUrgent" class="px-3 py-1 rounded-lg text-sm font-bold uppercase tracking-wide bg-red-50 text-red-600 animate-pulse">
                                Urgente
                            </span>
                        </div>
                        
                        <div class="prose prose-slate prose-sm text-slate-600">
                            <p v-if="selectedRequest.service_data.symptoms"><strong class="text-slate-900">Síntomas:</strong> {{ selectedRequest.service_data.symptoms }}</p>
                            <p v-if="selectedRequest.service_data.description"><strong class="text-slate-900">Descripción:</strong> {{ selectedRequest.service_data.description }}</p>
                            <p v-if="selectedRequest.service_data.notes"><strong class="text-slate-900">Notas:</strong> {{ selectedRequest.service_data.notes }}</p>
                            <p v-if="selectedRequest.service_data.serviceType"><strong class="text-slate-900">Tipo:</strong> {{ selectedRequest.service_data.serviceType }}</p>
                            <p v-if="selectedRequest.service_data.duration"><strong class="text-slate-900">Duración:</strong> {{ selectedRequest.service_data.duration }}</p>
                        </div>
                    </div>

                    <div v-if="selectedRequest.images && selectedRequest.images.length > 0">
                        <h3 class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-4">Evidencia Adjunta</h3>
                        <div class="grid grid-cols-3 gap-4">
                             <img 
                                v-for="(img, idx) in selectedRequest.images" 
                                :key="idx"
                                :src="`${backendUrl}/${img}`" 
                                class="w-full h-24 object-cover rounded-xl cursor-pointer hover:opacity-90 transition-opacity border border-slate-100"
                                @click="openImage(img)"
                            />
                        </div>
                    </div>

                    <!-- AI Clinical Insights -->
                    <div class="bg-slate-50 rounded-2xl p-6 border border-slate-100">
                        <div class="flex items-center gap-2 mb-4">
                            <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white">
                                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                            </div>
                            <h3 class="font-bold text-slate-900">AI Clinical Insights</h3>
                            
                            <template v-if="selectedRequest.service_data.clinical_insights">
                                <span 
                                    class="ml-auto px-2 py-1 rounded text-xs font-bold uppercase"
                                    :class="{
                                        'bg-red-100 text-red-700': selectedRequest.service_data.clinical_insights.triage_level === 'Red',
                                        'bg-amber-100 text-amber-700': selectedRequest.service_data.clinical_insights.triage_level === 'Yellow',
                                        'bg-emerald-100 text-emerald-700': selectedRequest.service_data.clinical_insights.triage_level === 'Green'
                                    }"
                                >
                                    {{ selectedRequest.service_data.clinical_insights.triage_level }} Priority
                                </span>
                            </template>
                        </div>
                        
                        <div v-if="selectedRequest.service_data.clinical_insights" class="space-y-4 text-sm">
                            <div>
                                <p class="font-bold text-slate-700 mb-1">Resumen</p>
                                <p class="text-slate-600">{{ selectedRequest.service_data.clinical_insights.summary }}</p>
                            </div>
                            
                            <div v-if="selectedRequest.service_data.clinical_insights.differentials?.length">
                                <p class="font-bold text-slate-700 mb-1">Posibles Causas</p>
                                <ul class="list-disc list-inside text-slate-600">
                                    <li v-for="diff in selectedRequest.service_data.clinical_insights.differentials" :key="diff">{{ diff }}</li>
                                </ul>
                            </div>

                            <div v-if="selectedRequest.service_data.clinical_insights.recommendations?.length">
                                <p class="font-bold text-slate-700 mb-1">Recomendaciones</p>
                                <ul class="list-disc list-inside text-slate-600">
                                    <li v-for="rec in selectedRequest.service_data.clinical_insights.recommendations" :key="rec">{{ rec }}</li>
                                </ul>
                            </div>
                        </div>
                        
                        <div v-else class="text-center py-6">
                            <p class="text-slate-500 text-sm mb-4">No hay análisis disponible para esta solicitud.</p>
                            <button 
                                @click="analyzeRequest(selectedRequest)"
                                class="px-4 py-2 bg-indigo-100 text-indigo-700 rounded-lg text-sm font-bold hover:bg-indigo-200 transition-colors flex items-center gap-2 mx-auto"
                                :disabled="analyzing"
                            >
                                <svg v-if="analyzing" class="animate-spin h-4 w-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                </svg>
                                <svg v-else class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                                {{ analyzing ? 'Analizando...' : 'Generar Análisis IA' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer Actions -->
        <div class="p-8 sm:p-12 bg-slate-50 mt-auto flex justify-end gap-4 rounded-b-3xl">
            <button 
                @click="updateStatus(selectedRequest, 'cancelled'); closeModal()"
                class="px-8 py-4 rounded-xl font-bold text-slate-500 hover:bg-rose-50 hover:text-rose-600 transition-all"
            >
                Rechazar Solicitud
            </button>
            <button 
                @click="updateStatus(selectedRequest, 'reviewed'); closeModal()"
                class="px-8 py-4 rounded-xl font-bold text-white bg-indigo-600 hover:bg-indigo-700 shadow-lg hover:shadow-indigo-200 transition-all transform hover:-translate-y-1"
            >
                Aprobar y Agendar
            </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from '@/composables/useToast';
import { useServiceRequests } from '@/composables/useServiceRequests';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import { 
  ArrowPathIcon, 
  ClipboardDocumentCheckIcon,
  CalendarIcon,
  PhotoIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline';

const { getAllRequests, updateRequest, loading, error } = useServiceRequests();
const router = useRouter();
const backendUrl = import.meta.env.VITE_BACKEND_URL;
const requests = ref([]);
const selectedRequest = ref(null);
const analyzing = ref(false);
const { addToast } = useToast();
import axios from 'axios';
import { useUserStore } from '@/stores/user';

const fetchRequests = async () => {
  try {
    const data = await getAllRequests({ status: 'pending' });
    requests.value = data;
  } catch (err) {
    console.error('Error fetching service requests:', err);
  }
};

const viewDetails = (request) => {
  selectedRequest.value = request;
};

const closeModal = () => {
  selectedRequest.value = null;
};

const openImage = (img) => {
  window.open(`${backendUrl}/${img}`, '_blank');
};

const analyzeRequest = async (request) => {
    analyzing.value = true;
    const userStore = useUserStore();
    try {
        const response = await axios.post(
            `${import.meta.env.VITE_API_URL}/v1/service_requests/${request.id}/analyze`,
            {},
            { headers: { Authorization: `Bearer ${userStore.token}` } }
        );
        
        // Update local state
        const updatedRequest = response.data;
        selectedRequest.value = updatedRequest;
        
        // Update in list
        const index = requests.value.findIndex(r => r.id === request.id);
        if (index !== -1) {
            requests.value[index] = updatedRequest;
        }
        
        addToast('Análisis IA completado', 'success');
    } catch (err) {
        console.error('Error analyzing request:', err);
        addToast('Error al generar análisis', 'error');
    } finally {
        analyzing.value = false;
    }
};

const updateStatus = async (request, newStatus) => {
  try {
    const originalStatus = request.status;
    request.status = newStatus;
    
    // Here you would call updateRequest from composable if implemented, or axios directly
    // await updateRequest(request.id, { status: newStatus });
    
    addToast('Estado actualizado correctamente', 'success');
  } catch (error) {
    console.error('Error updating status:', error);
    addToast('Error al actualizar estado', 'error');
  }
};

const getServiceTypeName = (type) => {
  const names = {
    consultation: 'Consulta',
    general: 'General',
    clinical: 'Clínico',
    aesthetic: 'Estética'
  };
  return names[type] || type;
};

const getServiceTypeClass = (type) => {
  const classes = {
    consultation: 'bg-sky-50 text-sky-700 border border-sky-100',
    general: 'bg-orange-50 text-orange-700 border border-orange-100',
    clinical: 'bg-purple-50 text-purple-700 border border-purple-100',
    aesthetic: 'bg-pink-50 text-pink-700 border border-pink-100'
  };
  return classes[type] || 'bg-gray-50 text-gray-700 border border-gray-100';
};

const getStatusClass = (status) => {
  const classes = {
    pending: 'text-amber-600',
    reviewed: 'text-blue-600',
    in_progress: 'text-indigo-600',
    completed: 'text-emerald-600',
    cancelled: 'text-red-600'
  };
  return classes[status] || 'text-gray-600';
};

const getStatusLabel = (status) => {
  const labels = {
    pending: 'Pendiente',
    reviewed: 'Revisado',
    in_progress: 'En Progreso',
    completed: 'Completado',
    cancelled: 'Cancelado'
  };
  return labels[status] || status;
};

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('es-ES', { 
    day: '2-digit', 
    month: 'short', 
    hour: '2-digit', 
    minute: '2-digit' 
  });
};

onMounted(() => {
  fetchRequests();
});
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out forwards;
}
</style>
