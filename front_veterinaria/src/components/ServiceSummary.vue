<template>
  <div class="space-y-8">
    <div class="text-center">
      <h3 class="text-2xl font-serif font-bold text-gray-900">Resumen de tu Solicitud</h3>
      <p class="text-gray-500 mt-2">Por favor verifica que toda la información sea correcta.</p>
    </div>

    <div class="bg-white rounded-3xl border border-gray-100 shadow-xl overflow-hidden max-w-2xl mx-auto">
      <!-- Header with Service Type -->
      <div class="bg-[#1BB0B9]/10 p-6 border-b border-[#1BB0B9]/10 flex items-center justify-between">
        <div class="flex items-center gap-4">
          <div class="p-3 bg-white rounded-xl text-[#1BB0B9] shadow-sm">
            <component :is="getServiceIcon(serviceType)" class="w-6 h-6" />
          </div>
          <div>
            <h4 class="font-bold text-gray-900 text-lg">{{ getServiceName(serviceType) }}</h4>
            <p class="text-sm text-gray-500">Servicio Veterinario</p>
          </div>
        </div>
        <div class="text-right">
          <p class="text-xs font-bold text-gray-400 uppercase tracking-wider">Costo Estimado</p>
          <p class="text-2xl font-serif font-bold text-[#1BB0B9]">S/. {{ estimatedCost }}</p>
        </div>
      </div>

      <div class="p-8 space-y-8">
        <!-- Date & Time -->
        <div class="flex items-start gap-4">
          <div class="p-2 bg-gray-50 rounded-lg text-gray-400 mt-1">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
          </div>
          <div class="flex-1">
            <h5 class="font-bold text-gray-900 mb-1">Fecha y Hora</h5>
            <div v-if="dateTime.isUrgent" class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-50 text-red-600 text-sm font-bold">
              <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
              Lo antes posible (Urgencia)
            </div>
            <div v-else class="text-gray-600">
              <p class="font-medium capitalize">{{ formatDate(dateTime.date) }}</p>
              <p class="text-sm">{{ getTimeSlotLabel(dateTime.timeSlot) }}</p>
            </div>
          </div>
          <button @click="$emit('edit', 2)" class="text-sm font-bold text-[#1BB0B9] hover:underline">Editar</button>
        </div>

        <div class="h-px bg-gray-100"></div>

        <!-- Pet Details -->
        <div class="flex items-start gap-4">
          <div class="p-2 bg-gray-50 rounded-lg text-gray-400 mt-1">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>
          </div>
          <div class="flex-1">
            <h5 class="font-bold text-gray-900 mb-1">Mascota</h5>
            <p class="text-gray-600 font-medium">{{ details.petName }}</p>
            <p class="text-sm text-gray-500 capitalize" v-if="details.species">{{ details.species }} {{ details.breed ? `• ${details.breed}` : '' }}</p>
          </div>
          <button @click="$emit('edit', 1)" class="text-sm font-bold text-[#1BB0B9] hover:underline">Editar</button>
        </div>

        <div class="h-px bg-gray-100"></div>

        <!-- Specific Details -->
        <div class="flex items-start gap-4">
          <div class="p-2 bg-gray-50 rounded-lg text-gray-400 mt-1">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
          </div>
          <div class="flex-1">
            <h5 class="font-bold text-gray-900 mb-1">Detalles</h5>
            
            <!-- Consultation -->
            <div v-if="serviceType === 'consultation'" class="space-y-2">
              <p class="text-sm text-gray-600"><span class="font-bold text-gray-400 text-xs uppercase">Síntomas:</span> {{ details.symptoms }}</p>
              <p class="text-sm text-gray-600"><span class="font-bold text-gray-400 text-xs uppercase">Duración:</span> {{ details.duration }}</p>
            </div>

            <!-- General -->
            <div v-if="serviceType === 'general'" class="space-y-2">
              <p class="text-sm text-gray-600"><span class="font-bold text-gray-400 text-xs uppercase">Tipo:</span> {{ details.serviceType }}</p>
              <p v-if="details.notes" class="text-sm text-gray-600"><span class="font-bold text-gray-400 text-xs uppercase">Notas:</span> {{ details.notes }}</p>
            </div>

            <!-- Clinical -->
            <div v-if="serviceType === 'clinical'" class="space-y-2">
              <p class="text-sm text-gray-600 line-clamp-2"><span class="font-bold text-gray-400 text-xs uppercase">Caso:</span> {{ details.description }}</p>
              <p class="text-sm text-gray-600"><span class="font-bold text-gray-400 text-xs uppercase">Tipo:</span> {{ details.isFollowUp ? 'Control / Seguimiento' : 'Primera Consulta' }}</p>
            </div>

            <!-- Aesthetic -->
            <div v-if="serviceType === 'aesthetic'" class="space-y-2">
              <div v-for="(service, idx) in details.services" :key="idx" class="text-sm text-gray-600">
                • {{ getAestheticLabel(service.type) }}
              </div>
            </div>
          </div>
          <button @click="$emit('edit', 1)" class="text-sm font-bold text-[#1BB0B9] hover:underline">Editar</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { 
  ClipboardDocumentListIcon, 
  HeartIcon, 
  BeakerIcon, 
  ScissorsIcon 
} from '@heroicons/vue/24/outline';

const props = defineProps({
  serviceType: String,
  details: Object,
  dateTime: Object,
  estimatedCost: Number
});

defineEmits(['edit']);

const getServiceIcon = (type) => {
  const icons = {
    consultation: ClipboardDocumentListIcon,
    general: HeartIcon,
    clinical: BeakerIcon,
    aesthetic: ScissorsIcon
  };
  return icons[type] || ClipboardDocumentListIcon;
};

const getServiceName = (type) => {
  const names = {
    consultation: 'Consulta Veterinaria',
    general: 'Servicios Generales',
    clinical: 'Caso Clínico',
    aesthetic: 'Estética & Spa'
  };
  return names[type] || type;
};

const formatDate = (date) => {
  if (!date) return '';
  return date.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
};

const getTimeSlotLabel = (slot) => {
  const slots = {
    morning: 'Mañana (8:00 AM - 12:00 PM)',
    afternoon: 'Tarde (12:00 PM - 5:00 PM)',
    evening: 'Noche (5:00 PM - 8:00 PM)'
  };
  return slots[slot] || slot;
};

const getAestheticLabel = (type) => {
  const labels = {
    'baño': 'Baño Completo',
    'corte': 'Corte de Pelo',
    'baño-corte': 'Baño + Corte',
    'uñas': 'Corte de Uñas',
    'limpieza-oidos': 'Limpieza de Oídos'
  };
  return labels[type] || type;
};
</script>
