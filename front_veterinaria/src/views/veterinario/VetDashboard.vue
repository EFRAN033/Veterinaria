<template>
  <div class="min-h-screen bg-slate-50/50 font-sans text-slate-600">
    
    <!-- Header Section -->
    <div class="bg-white border-b border-slate-200">
      <div class="px-8 py-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 class="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Squares2X2Icon class="h-7 w-7 text-indigo-600" />
            Panel de Control
          </h1>
          <p class="text-sm text-slate-500 mt-1">Bienvenido, Dr. {{ userStore.userName || 'Veterinario' }}</p>
        </div>
        
        <div class="flex items-center gap-3">
          <p class="text-sm font-medium text-slate-500 bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
            {{ currentDate }}
          </p>
          <button 
            @click="refreshData" 
            class="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors border border-transparent hover:border-indigo-100"
            :disabled="loading"
            title="Actualizar datos"
          >
            <ArrowPathIcon class="h-5 w-5" :class="{ 'animate-spin': loading }" />
          </button>
        </div>
      </div>
    </div>

    <div class="p-8 max-w-[1600px] mx-auto space-y-8">
      
      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- Stat Card 1 -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 flex items-center gap-4 group hover:border-indigo-300 transition-all">
          <div class="p-3 bg-indigo-50 rounded-xl text-indigo-600 group-hover:bg-indigo-600 group-hover:text-white transition-colors">
            <CalendarDaysIcon class="h-6 w-6" />
          </div>
          <div>
            <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Citas Hoy</p>
            <p class="text-2xl font-bold text-slate-800">{{ todayAppointments.length }}</p>
          </div>
        </div>

        <!-- Stat Card 2 -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 flex items-center gap-4 group hover:border-amber-300 transition-all">
          <div class="p-3 bg-amber-50 rounded-xl text-amber-600 group-hover:bg-amber-500 group-hover:text-white transition-colors">
            <InboxArrowDownIcon class="h-6 w-6" />
          </div>
          <div>
            <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Solicitudes</p>
            <p class="text-2xl font-bold text-slate-800">{{ pendingRequestsCount }}</p>
          </div>
        </div>

        <!-- Stat Card 3 -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 flex items-center gap-4 group hover:border-rose-300 transition-all">
          <div class="p-3 bg-rose-50 rounded-xl text-rose-600 group-hover:bg-rose-500 group-hover:text-white transition-colors">
            <ExclamationTriangleIcon class="h-6 w-6" />
          </div>
          <div>
            <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Urgencias</p>
            <p class="text-2xl font-bold text-slate-800">{{ urgentCount }}</p>
          </div>
        </div>

        <!-- Stat Card 4 -->
        <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 flex items-center gap-4 group hover:border-emerald-300 transition-all">
          <div class="p-3 bg-emerald-50 rounded-xl text-emerald-600 group-hover:bg-emerald-500 group-hover:text-white transition-colors">
            <CheckBadgeIcon class="h-6 w-6" />
          </div>
          <div>
            <p class="text-xs font-bold text-slate-400 uppercase tracking-wider">Completadas</p>
            <p class="text-2xl font-bold text-slate-800">{{ completedCount }}</p>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
        
        <!-- Main Content Column (Left) -->
        <div class="xl:col-span-2 space-y-8">
          
          <!-- Quick Actions -->
          <div class="bg-gradient-to-r from-indigo-600 to-purple-700 rounded-2xl p-6 shadow-lg text-white relative overflow-hidden">
            <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full -translate-y-1/2 translate-x-1/4 pointer-events-none"></div>
            
            <h2 class="text-lg font-bold mb-4 relative z-10">Acciones Rápidas</h2>
            <div class="flex flex-wrap gap-4 relative z-10">
              <button @click="$router.push('/veterinario/citas')" class="flex items-center gap-2 px-4 py-2.5 bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-xl font-medium transition-all border border-white/10">
                <PlusIcon class="h-5 w-5" />
                Nueva Cita
              </button>
              <button @click="$router.push('/veterinario/chat')" class="flex items-center gap-2 px-4 py-2.5 bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-xl font-medium transition-all border border-white/10">
                <SparklesIcon class="h-5 w-5" />
                Asistente IA
              </button>
              <button class="flex items-center gap-2 px-4 py-2.5 bg-white/10 hover:bg-white/20 backdrop-blur-sm rounded-xl font-medium transition-all border border-white/10">
                <UserPlusIcon class="h-5 w-5" />
                Registrar Paciente
              </button>
            </div>
          </div>

          <!-- Service Requests (Existing Component) -->
          <div>
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-lg font-bold text-slate-800">Solicitudes Entrantes</h2>
              <span class="text-xs font-medium text-slate-500 bg-white px-2 py-1 rounded border border-slate-200">Pendientes de revisión</span>
            </div>
            <ServiceRequestsList />
          </div>

        </div>

        <!-- Sidebar Column (Right) -->
        <div class="space-y-8">
          
          <!-- Today's Agenda (Mini) -->
          <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col h-[500px]">
            <div class="p-4 border-b border-slate-100 flex justify-between items-center bg-slate-50/50">
              <h2 class="font-bold text-slate-800 flex items-center gap-2">
                <ClockIcon class="h-5 w-5 text-indigo-600" />
                Agenda de Hoy
              </h2>
              <router-link to="/veterinario/citas" class="text-xs font-bold text-indigo-600 hover:text-indigo-800">Ver todo</router-link>
            </div>
            
            <div class="flex-1 overflow-y-auto p-4 space-y-3 custom-scrollbar">
              <div v-if="todayAppointments.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400 opacity-60 text-center">
                <CalendarDaysIcon class="h-12 w-12 mb-2" />
                <p class="text-sm font-medium">No hay citas para hoy</p>
              </div>

              <div 
                v-for="app in todayAppointments" 
                :key="app.id"
                class="flex gap-3 p-3 rounded-xl border border-slate-100 hover:border-indigo-200 hover:bg-slate-50 transition-all group"
              >
                <div class="flex flex-col items-center justify-center min-w-[3.5rem] bg-slate-100 rounded-lg p-2 h-fit">
                  <span class="text-xs font-bold text-slate-500">{{ app.appointment_time.substring(0, 5) }}</span>
                </div>
                
                <div class="flex-1 min-w-0">
                  <h4 class="font-bold text-slate-800 text-sm truncate">{{ app.pet_name || 'Mascota #' + app.pet_id }}</h4>
                  <p class="text-xs text-slate-500 truncate">Cliente #{{ app.user_id }}</p>
                  
                  <div class="flex items-center gap-2 mt-2">
                    <span class="text-[10px] px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-600 font-medium border border-indigo-100 truncate max-w-full">
                      {{ app.service_id || 'Consulta' }}
                    </span>
                    <button 
                      @click.stop="$router.push(`/veterinario/chat?petId=${app.pet_id}&petName=${app.pet_name || 'Paciente'}&requestId=${app.id}`)"
                      class="p-1 text-indigo-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-full transition-colors"
                      title="Consultar con IA"
                    >
                      <SparklesIcon class="h-4 w-4" />
                    </button>
                  </div>
                </div>
              </div>
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
import { useServiceRequests } from '@/composables/useServiceRequests';
import ServiceRequestsList from '@/components/ServiceRequestsList.vue';
import { 
  Squares2X2Icon,
  ArrowPathIcon,
  CalendarDaysIcon,
  InboxArrowDownIcon,
  ExclamationTriangleIcon,
  CheckBadgeIcon,
  PlusIcon,
  SparklesIcon,
  UserPlusIcon,
  ClockIcon
} from '@heroicons/vue/24/outline';

const userStore = useUserStore();
const { getAllRequests } = useServiceRequests();

const loading = ref(false);
const allAppointments = ref([]);
const serviceRequests = ref([]);

const currentDate = computed(() => {
  return new Date().toLocaleDateString('es-ES', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
});

const todayAppointments = computed(() => {
  const today = new Date().toISOString().split('T')[0];
  return allAppointments.value
    .filter(app => app.appointment_date === today)
    .sort((a, b) => a.appointment_time.localeCompare(b.appointment_time));
});

const pendingRequestsCount = computed(() => {
  return serviceRequests.value.filter(req => req.status === 'pending').length;
});

const urgentCount = computed(() => {
  const urgentApps = allAppointments.value.filter(app => 
    app.notes && (app.notes.toLowerCase().includes('urgente') || app.notes.toLowerCase().includes('dolor'))
  ).length;
  
  const urgentReqs = serviceRequests.value.filter(req => 
    (req.service_data && req.service_data.urgency === 'alta') ||
    (req.service_data && req.service_data.isUrgent === true)
  ).length;
  
  return urgentApps + urgentReqs;
});

const completedCount = computed(() => {
  return allAppointments.value.filter(app => app.status === 'completed' || app.status === 'confirmed').length;
});

const refreshData = async () => {
  loading.value = true;
  try {
    const [appsRes, reqsData] = await Promise.all([
      axios.get(`${import.meta.env.VITE_API_URL}/v1/appointments/all`, {
        headers: { Authorization: `Bearer ${userStore.token}` }
      }),
      getAllRequests()
    ]);
    
    allAppointments.value = appsRes.data;
    serviceRequests.value = reqsData;
  } catch (err) {
    console.error('Error refreshing dashboard:', err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  refreshData();
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
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