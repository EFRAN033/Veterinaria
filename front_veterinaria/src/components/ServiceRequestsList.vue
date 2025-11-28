<template>
  <div class="bg-white rounded-2xl shadow-lg p-6 border border-slate-100">
    <div class="flex justify-between items-center mb-6">
      <div>
        <h3 class="text-xl font-bold text-slate-900">Solicitudes de Servicio</h3>
        <p class="text-sm text-slate-500 mt-1">Nuevas solicitudes de clientes</p>
      </div>
      <button 
        @click="fetchRequests" 
        class="p-2 rounded-lg text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors"
        :disabled="loading"
      >
        <ArrowPathIcon class="h-5 w-5" :class="{ 'animate-spin': loading }" />
      </button>
    </div>

    <div v-if="loading" class="flex justify-center py-8">
      <LoadingSpinner />
    </div>

    <div v-else-if="error" class="text-center py-8">
      <p class="text-red-500 text-sm">{{ error }}</p>
      <button @click="fetchRequests" class="mt-2 text-xs text-indigo-600 hover:underline">Reintentar</button>
    </div>

    <div v-else-if="requests.length === 0" class="text-center py-12">
      <ClipboardDocumentCheckIcon class="h-16 w-16 mx-auto text-slate-200 mb-4" />
      <p class="text-slate-400 text-sm">No hay solicitudes pendientes</p>
    </div>

    <div v-else class="space-y-3 max-h-[600px] overflow-y-auto custom-scrollbar">
      <div 
        v-for="request in requests" 
        :key="request.id"
        class="p-4 border border-slate-100 rounded-xl hover:shadow-md hover:border-indigo-200 transition-all cursor-pointer group"
        @click="viewDetails(request)"
      >
        <div class="flex justify-between items-start mb-3">
          <div class="flex-1">
            <div class="flex items-center gap-2 mb-1">
              <h4 class="font-bold text-slate-800">{{ request.pet_name || 'Sin nombre' }}</h4>
              <span class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase" :class="getServiceTypeClass(request.service_type)">
                {{ getServiceTypeName(request.service_type) }}
              </span>
            </div>
            <p class="text-sm text-slate-500">{{ request.user_name || `Cliente #${request.user_id}` }}</p>
            <p class="text-xs text-slate-400">{{ request.user_email }}</p>
          </div>
          <div class="text-right">
            <span class="px-3 py-1 rounded-full text-xs font-bold" :class="getStatusClass(request.status)">
              {{ getStatusLabel(request.status) }}
            </span>
            <p class="text-sm font-bold text-slate-700 mt-2">S/. {{ request.estimated_cost }}</p>
          </div>
        </div>

        <div class="flex items-center gap-4 text-xs text-slate-500 mb-3">
          <span class="flex items-center gap-1">
            <CalendarIcon class="h-4 w-4" />
            {{ formatDate(request.created_at) }}
          </span>
          <span v-if="request.images && request.images.length > 0" class="flex items-center gap-1">
            <PhotoIcon class="h-4 w-4" />
            {{ request.images.length }} foto{{ request.images.length > 1 ? 's' : '' }}
          </span>
        </div>

        <!-- Preview of service data -->
        <!-- Common Scheduling Info -->
        <div class="mb-3 p-3 bg-slate-50 rounded-lg border border-slate-100">
          <div v-if="request.service_data.isUrgent" class="flex items-center gap-2 text-red-600 font-bold text-xs mb-1">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
            </span>
            SOLICITUD URGENTE (Lo antes posible)
          </div>
          <div v-else-if="request.service_data.preferredDate" class="flex items-center gap-4 text-xs text-slate-600">
            <div class="flex items-center gap-1.5">
              <CalendarIcon class="h-4 w-4 text-slate-400" />
              <span class="font-medium capitalize">{{ formatDateFriendly(request.service_data.preferredDate) }}</span>
            </div>
            <div class="flex items-center gap-1.5">
              <ClockIcon class="h-4 w-4 text-slate-400" />
              <span class="font-medium">{{ translateTimeSlot(request.service_data.preferredTime) }}</span>
            </div>
          </div>
          <div v-else class="text-xs text-slate-400 italic">
            Sin preferencia de horario especificada
          </div>
        </div>

        <!-- Specific Service Data -->
        <div v-if="request.service_data" class="text-xs text-slate-600 space-y-1 px-1">
          <template v-if="request.service_type === 'consultation'">
            <p><span class="font-bold text-slate-400 uppercase text-[10px] tracking-wider">Especie:</span> {{ request.service_data.species }}</p>
            <p class="line-clamp-2"><span class="font-bold text-slate-400 uppercase text-[10px] tracking-wider">Síntomas:</span> {{ request.service_data.symptoms }}</p>
          </template>
          
          <template v-else-if="request.service_type === 'general'">
            <p><span class="font-bold text-slate-400 uppercase text-[10px] tracking-wider">Servicio:</span> {{ request.service_data.serviceType }}</p>
            <p v-if="request.service_data.notes" class="line-clamp-2"><span class="font-bold text-slate-400 uppercase text-[10px] tracking-wider">Notas:</span> {{ request.service_data.notes }}</p>
          </template>
          
          <template v-else-if="request.service_type === 'clinical'">
            <p class="line-clamp-2"><span class="font-bold text-slate-400 uppercase text-[10px] tracking-wider">Caso:</span> {{ request.service_data.description }}</p>
            <p><span class="font-bold text-slate-400 uppercase text-[10px] tracking-wider">Tipo:</span> {{ request.service_data.isFollowUp ? 'Control' : 'Primera vez' }}</p>
          </template>
          
          <template v-else-if="request.service_type === 'aesthetic'">
            <p><span class="font-bold text-slate-400 uppercase text-[10px] tracking-wider">Raza:</span> {{ request.service_data.breed }}</p>
            <p><span class="font-bold text-slate-400 uppercase text-[10px] tracking-wider">Servicios:</span> {{ request.service_data.services?.length || 0 }} seleccionados</p>
          </template>
        </div>

        <!-- Image previews -->
        <div v-if="request.images && request.images.length > 0" class="flex gap-2 mt-3">
          <img 
            v-for="(img, idx) in request.images.slice(0, 4)" 
            :key="idx"
            :src="`${backendUrl}/${img}`" 
            class="w-16 h-16 object-cover rounded-lg border border-slate-200"
            @error="handleImageError"
          />
          <div v-if="request.images.length > 4" 
               class="w-16 h-16 bg-slate-100 rounded-lg flex items-center justify-center text-sm font-bold text-slate-500">
            +{{ request.images.length - 4 }}
          </div>
        </div>

        <!-- Quick actions -->
        <div class="flex gap-2 mt-3 pt-3 border-t border-slate-100 opacity-0 group-hover:opacity-100 transition-opacity">
          <button 
            @click.stop="updateStatus(request.id, 'reviewed')"
            class="flex-1 px-3 py-2 text-xs font-bold text-indigo-600 bg-indigo-50 rounded-lg hover:bg-indigo-100 transition-colors"
          >
            Marcar como Revisado
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
  ClockIcon
} from '@heroicons/vue/24/outline';

const { getAllRequests, updateRequest, loading, error } = useServiceRequests();
const router = useRouter(); // Added router
const backendUrl = import.meta.env.VITE_BACKEND_URL; // Added backendUrl
const requests = ref([]);

const fetchRequests = async () => {
  try {
    const data = await getAllRequests({ status: 'pending' });
    requests.value = data;
  } catch (err) {
    console.error('Error fetching service requests:', err);
  }
};

const viewDetails = (request) => {
  console.log('View details:', request);
  addToast(`Detalles de solicitud #${request.id}\n\nEsta funcionalidad se implementará próximamente.`, 'info');
};

const updateStatus = async (request, newStatus) => {
  try {
    const originalStatus = request.status;
    request.status = newStatus;
    
    
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
    consultation: 'bg-sky-100 text-sky-700', // Celeste (IA/Consulta)
    general: 'bg-orange-100 text-orange-700', // Naranja (Nutrición/General)
    clinical: 'bg-purple-100 text-purple-700', // Clínico (Mantenemos purple o cambiamos si se pide)
    aesthetic: 'bg-pink-100 text-pink-700' // Rosado (Estética)
  };
  return classes[type] || 'bg-gray-100 text-gray-700';
};

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-amber-100 text-amber-700',
    reviewed: 'bg-blue-100 text-blue-700',
    in_progress: 'bg-indigo-100 text-indigo-700',
    completed: 'bg-emerald-100 text-emerald-700',
    cancelled: 'bg-red-100 text-red-700'
  };
  return classes[status] || 'bg-gray-100 text-gray-700';
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

const formatDateFriendly = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('es-ES', { weekday: 'short', day: 'numeric', month: 'short' });
};

const translateTimeSlot = (slot) => {
  const slots = {
    morning: 'Mañana',
    afternoon: 'Tarde',
    evening: 'Noche'
  };
  return slots[slot] || slot;
};

const handleImageError = (e) => {
  e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="100" height="100"%3E%3Crect fill="%23f1f5f9" width="100" height="100"/%3E%3Ctext x="50%25" y="50%25" dominant-baseline="middle" text-anchor="middle" fill="%2394a3b8" font-size="12"%3ENo disponible%3C/text%3E%3C/svg%3E';
};

onMounted(() => {
  fetchRequests();
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
</style>
