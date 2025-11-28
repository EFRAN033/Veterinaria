<template>
  <div class="min-h-screen bg-gray-50 flex flex-col relative overflow-hidden">
    <!-- Decorative Background Elements -->
    <div class="absolute top-0 right-0 w-[500px] h-[500px] bg-[#1BB0B9]/10 rounded-full blur-[100px] pointer-events-none translate-x-1/3 -translate-y-1/3"></div>
    <div class="absolute bottom-0 left-0 w-[500px] h-[500px] bg-[#BEDC74]/20 rounded-full blur-[100px] pointer-events-none -translate-x-1/3 translate-y-1/3"></div>

    <!-- Back Button -->
    <BackButton />

    <!-- Main Content -->
    <main class="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-12 relative z-10">
      <div class="max-w-5xl mx-auto">
        
        <!-- Header Section -->
        <div class="mb-12 mt-8">
          <h1 class="text-5xl font-serif font-bold text-gray-900 mb-4 tracking-tight">
            Mis <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#16aeb1] to-[#1BB0B9]">Citas</span>
          </h1>
          <p class="text-xl text-gray-500 font-light max-w-2xl">
            Gestiona tus próximas visitas y revisa tu historial de atención veterinaria.
          </p>
        </div>

        <div v-if="loading" class="flex justify-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#1BB0B9]"></div>
        </div>

        <div v-else-if="error" class="text-red-500 text-lg font-medium mb-8 bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
          {{ error }}
        </div>

        <div v-else>
          <div v-if="appointments.length === 0" class="text-center py-20">
            <div class="bg-gray-100 rounded-full h-24 w-24 flex items-center justify-center mx-auto mb-6">
              <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-2">No tienes citas programadas</h3>
            <p class="text-gray-500 mb-8 max-w-md mx-auto">Agenda una cita para el cuidado de tus mascotas con nuestros especialistas.</p>
            <router-link to="/servicios" class="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-full shadow-sm text-white bg-gradient-to-r from-[#16aeb1] to-[#1BB0B9] hover:from-[#149ea1] hover:to-[#189ea6] transition-all transform hover:scale-105">
              Agendar Nueva Cita
            </router-link>
          </div>

          <div v-else class="space-y-8">
            <!-- Appointment List -->
            <div v-for="appointment in appointments" :key="appointment.id" class="group border-b border-gray-200 pb-8 hover:border-[#1BB0B9]/30 transition-colors">
              <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
                
                <!-- Date & Time -->
                <div class="flex items-start gap-6">
                  <div class="flex flex-col items-center justify-center w-20 h-20 bg-white border border-gray-200 rounded-2xl shadow-sm group-hover:border-[#1BB0B9] group-hover:shadow-md transition-all">
                    <span class="text-xs font-bold text-gray-400 uppercase">{{ getMonth(appointment.date) }}</span>
                    <span class="text-3xl font-bold text-gray-900">{{ getDay(appointment.date) }}</span>
                  </div>
                  
                  <div>
                    <div class="flex items-center gap-3 mb-1">
                      <h3 class="text-2xl font-bold text-gray-900 group-hover:text-[#1BB0B9] transition-colors">
                        {{ appointment.service_name || 'Consulta General' }}
                      </h3>
                      <span :class="getStatusClass(appointment.status)" class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wide">
                        {{ getStatusLabel(appointment.status) }}
                      </span>
                    </div>
                    <div class="flex items-center gap-6 text-gray-500">
                      <div class="flex items-center gap-2">
                        <svg class="w-5 h-5 text-[#1BB0B9]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <span class="font-medium">{{ formatTime(appointment.time) }}</span>
                      </div>
                      <div class="flex items-center gap-2">
                        <svg class="w-5 h-5 text-[#1BB0B9]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                        <span class="font-medium">{{ appointment.pet_name || 'Mascota' }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Actions -->
                <div class="flex items-center gap-3">
                  <button class="px-4 py-2 text-sm font-bold text-gray-600 hover:text-[#1BB0B9] transition-colors">
                    Ver Detalles
                  </button>
                  <button v-if="appointment.status === 'pending'" class="px-4 py-2 text-sm font-bold text-red-500 hover:text-red-600 transition-colors">
                    Cancelar
                  </button>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import BackButton from '@/components/BackButton.vue';
import Footer from './Footer.vue';

const userStore = useUserStore();
const appointments = ref([]);
const loading = ref(true);
const error = ref(null);

const getMonth = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).toLocaleDateString('es-ES', { month: 'short' }).replace('.', '');
};

const getDay = (dateString) => {
  if (!dateString) return '';
  return new Date(dateString).getDate();
};

const formatTime = (timeString) => {
  if (!timeString) return '';
  return timeString.substring(0, 5);
};

const getStatusLabel = (status) => {
  const labels = {
    pending: 'Pendiente',
    confirmed: 'Confirmada',
    completed: 'Completada',
    cancelled: 'Cancelada'
  };
  return labels[status] || status;
};

const getStatusClass = (status) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-700',
    confirmed: 'bg-blue-100 text-blue-700',
    completed: 'bg-green-100 text-green-700',
    cancelled: 'bg-red-100 text-red-700'
  };
  return classes[status] || 'bg-gray-100 text-gray-700';
};

onMounted(async () => {
  try {
    loading.value = true;
    appointments.value = await userStore.fetchAppointments();
  } catch (e) {
    error.value = 'No se pudieron cargar tus citas. Por favor, intenta de nuevo.';
    console.error(e);
  } finally {
    loading.value = false;
  }
});
</script>
