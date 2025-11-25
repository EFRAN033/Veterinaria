<template>
  <div class="h-screen bg-slate-50 flex flex-col p-6 font-sans text-slate-600 overflow-hidden">
    
    <div class="grid grid-cols-12 gap-6 mb-6 shrink-0">
      
      <div class="col-span-12 lg:col-span-3 flex flex-col justify-center">
        <h1 class="text-xl font-bold text-slate-800 tracking-tight flex items-center gap-2">
          <CalendarDaysIcon class="h-6 w-6 text-indigo-800" /> Agenda Veterinaria
        </h1>
        <p class="text-xs text-slate-500 mt-1">Panel de control de turnos</p>
      </div>

      <div class="col-span-12 lg:col-span-9 grid grid-cols-3 gap-4">
        
        <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between group hover:border-indigo-200 transition-colors">
          <div>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Citas Hoy</p>
            <p class="text-lg font-bold text-slate-800">{{ metrics.today }}</p>
          </div>
          <div class="p-2 bg-indigo-800 rounded-lg text-white shadow-md shadow-indigo-200">
            <ClockIcon class="h-5 w-5" />
          </div>
        </div>

        <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between group hover:border-indigo-200 transition-colors">
          <div>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Pendientes</p>
            <p class="text-lg font-bold text-amber-600">{{ metrics.pending }}</p>
          </div>
          <div class="p-2 bg-indigo-800 rounded-lg text-white shadow-md shadow-indigo-200">
            <ExclamationCircleIcon class="h-5 w-5" />
          </div>
        </div>

        <div class="bg-white p-3 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between group hover:border-indigo-200 transition-colors">
          <div>
            <p class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Confirmadas</p>
            <p class="text-lg font-bold text-emerald-600">{{ metrics.confirmed }}</p>
          </div>
          <div class="p-2 bg-indigo-800 rounded-lg text-white shadow-md shadow-indigo-200">
            <CheckBadgeIcon class="h-5 w-5" />
          </div>
        </div>
      </div>
    </div>

    <div class="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 min-h-0"> 
      
      <div class="lg:col-span-8 xl:col-span-9 bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden flex flex-col">
        <div class="flex-1 p-2">
          <FullCalendar :options="calendarOptions" class="micro-calendar h-full" />
        </div>
      </div>

      <div class="lg:col-span-4 xl:col-span-3 flex flex-col gap-4 h-full min-h-0">
        
        <div class="bg-white p-3 rounded-xl shadow-sm border border-slate-200 shrink-0 space-y-3">
          <div class="relative">
            <input 
              v-model="searchQuery" 
              type="text" 
              placeholder="Buscar cliente o mascota..." 
              class="w-full pl-9 pr-3 py-2 text-xs font-medium text-slate-700 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent placeholder-slate-400 transition-all"
            />
            <MagnifyingGlassIcon class="h-4 w-4 text-slate-400 absolute left-3 top-2" />
          </div>

          <div class="flex justify-between gap-1">
            <button 
              v-for="filter in filters" :key="filter.id"
              @click="activeFilter = filter.id"
              class="flex-1 py-1.5 text-[10px] font-bold rounded-md border transition-all duration-200 flex justify-center items-center gap-1"
              :class="activeFilter === filter.id 
                ? 'bg-indigo-800 text-white border-indigo-800' 
                : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50'"
            >
              <component :is="filter.icon" class="h-3 w-3" />
              {{ filter.label }}
            </button>
          </div>
        </div>

        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 flex-1 overflow-hidden flex flex-col">
          <div class="bg-slate-50 px-4 py-2 border-b border-slate-200 shrink-0 flex justify-between items-center">
            <h3 class="text-[11px] font-bold uppercase text-slate-500 tracking-wider">
              {{ selectedDate ? formatDateHeader(selectedDate) : 'Agenda Global' }}
            </h3>
            <span class="bg-white border border-slate-200 text-slate-600 text-[10px] font-bold px-2 py-0.5 rounded-full shadow-sm">
              {{ filteredList.length }}
            </span>
          </div>
          
          <div class="overflow-y-auto p-3 space-y-2 custom-scrollbar flex-1">
            <div v-if="filteredList.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400 space-y-2 opacity-60">
              <InboxIcon class="h-8 w-8" />
              <p class="text-xs font-medium">No se encontraron citas</p>
            </div>
            
            <div 
              v-for="app in filteredList" 
              :key="app.id" 
              class="group relative bg-white p-3 rounded-lg border border-slate-200 hover:border-indigo-400 hover:shadow-md transition-all duration-200 cursor-pointer"
              @click="openDetails(app)"
            >
              <div class="absolute left-0 top-0 bottom-0 w-1 rounded-l-lg transition-colors" :class="getStatusBorder(app.extendedProps.status)"></div>
              
              <div class="pl-2 flex justify-between items-start">
                <div class="overflow-hidden w-full">
                  <div class="flex justify-between items-center mb-1">
                    <span class="text-[10px] font-mono font-bold text-slate-600 bg-slate-100 px-1.5 py-0.5 rounded border border-slate-200">
                      {{ app.extendedProps.time }}
                    </span>
                    <span class="text-[9px] font-bold uppercase px-1.5 rounded text-slate-500 bg-slate-50">
                      {{ app.extendedProps.statusLabel }}
                    </span>
                  </div>
                  
                  <h4 class="text-xs font-bold text-slate-800 truncate">{{ app.title }}</h4>
                  
                  <div class="flex items-center gap-3 mt-1.5">
                    <div class="flex items-center gap-1 text-[10px] text-slate-500 truncate max-w-[50%]">
                      <UserIcon class="h-3 w-3 text-slate-400 shrink-0" /> 
                      <span class="truncate">{{ app.extendedProps.client }}</span>
                    </div>
                    <div class="flex items-center gap-1 text-[10px] text-slate-500 truncate max-w-[50%]">
                      <TagIcon class="h-3 w-3 text-slate-400 shrink-0" /> 
                      <span class="truncate">{{ app.extendedProps.pet }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/30 backdrop-blur-sm" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-sm overflow-hidden border border-slate-200 transform transition-all">
        
        <div class="bg-indigo-800 px-5 py-4 flex justify-between items-center">
          <div>
            <p class="text-[10px] font-bold text-indigo-200 uppercase tracking-widest">Detalle de Cita</p>
            <h3 class="text-sm font-bold text-white mt-0.5">ID #{{ selectedEvent.id }}</h3>
          </div>
          <button @click="closeModal" class="text-indigo-200 hover:text-white transition-colors">
            <XMarkIcon class="h-5 w-5"/>
          </button>
        </div>

        <div class="p-5 space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="space-y-1">
              <span class="text-[10px] font-semibold text-slate-400 uppercase">Fecha</span>
              <p class="text-xs font-bold text-slate-700 flex items-center gap-1">
                <CalendarDaysIcon class="h-3 w-3 text-indigo-600" />
                {{ formatFullDate(selectedEvent.start) }}
              </p>
            </div>
            <div class="space-y-1">
              <span class="text-[10px] font-semibold text-slate-400 uppercase">Hora</span>
              <p class="text-xs font-bold text-slate-700 flex items-center gap-1">
                <ClockIcon class="h-3 w-3 text-indigo-600" />
                {{ selectedEvent.time }}
              </p>
            </div>
          </div>

          <div class="border-t border-slate-100 pt-3 space-y-3">
            <div class="flex items-start gap-3">
              <div class="mt-0.5 p-1.5 bg-indigo-50 rounded-md text-indigo-600">
                <UserIcon class="h-4 w-4" />
              </div>
              <div>
                <p class="text-[10px] font-bold text-slate-400 uppercase">Cliente</p>
                <p class="text-xs font-medium text-slate-700">{{ selectedEvent.client }}</p>
              </div>
            </div>
            
            <div class="flex items-start gap-3">
              <div class="mt-0.5 p-1.5 bg-purple-50 rounded-md text-purple-600">
                <TagIcon class="h-4 w-4" />
              </div>
              <div>
                <p class="text-[10px] font-bold text-slate-400 uppercase">Mascota</p>
                <p class="text-xs font-medium text-slate-700">{{ selectedEvent.pet }}</p>
              </div>
            </div>
          </div>

          <div v-if="selectedEvent.notes" class="bg-yellow-50 border border-yellow-100 p-3 rounded-lg">
            <p class="text-[10px] font-bold text-yellow-700 uppercase mb-1 flex items-center gap-1">
              <DocumentTextIcon class="h-3 w-3" /> Notas
            </p>
            <p class="text-xs text-slate-600 italic">"{{ selectedEvent.notes }}"</p>
          </div>
        </div>
        
        <div class="bg-slate-50 px-5 py-3 border-t border-slate-200 text-right">
          <button @click="closeModal" class="text-xs font-bold text-slate-600 hover:text-slate-900 px-4 py-2 bg-white border border-slate-300 rounded-lg shadow-sm transition-colors">
            Cerrar
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import listPlugin from '@fullcalendar/list';
import esLocale from '@fullcalendar/core/locales/es';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { 
  CalendarDaysIcon, UserIcon, ClockIcon, TagIcon, 
  MagnifyingGlassIcon, FunnelIcon, CheckBadgeIcon, 
  ExclamationCircleIcon, XMarkIcon, DocumentTextIcon,
  InboxIcon
} from '@heroicons/vue/24/outline';
import { useServiceRequests } from '@/composables/useServiceRequests';

const { getAllRequests } = useServiceRequests();

const userStore = useUserStore();
const isModalOpen = ref(false);
const selectedEvent = ref({});
const selectedDate = ref(null); 
const allEvents = ref([]); 
const activeFilter = ref('all'); 
const searchQuery = ref(''); 

const filters = [
  { id: 'all', label: 'Todo', icon: FunnelIcon },
  { id: 'confirmed', label: 'Ok', icon: CheckBadgeIcon },
  { id: 'pending', label: 'Pend.', icon: ExclamationCircleIcon },
  { id: 'cancelled', label: 'Canc.', icon: XMarkIcon }
];

// Configuración del Calendario Compacto
const calendarOptions = ref({
  plugins: [dayGridPlugin, interactionPlugin, listPlugin],
  initialView: 'dayGridMonth',
  locale: esLocale,
  height: '100%', 
  headerToolbar: { left: 'title', center: '', right: 'prev,next' },
  dayMaxEvents: 1, 
  fixedWeekCount: false, 
  events: [],
  dateClick: handleDateClick,
  eventClick: handleEventClick,
  editable: false,
  eventContent: renderEventContent, // Custom render function
});

function renderEventContent(arg) {
  const props = arg.event.extendedProps;
  return {
    html: `
      <div class="flex flex-col gap-0.5 overflow-hidden">
        <div class="flex items-center gap-1">
          <span class="text-[9px] font-bold bg-white/80 px-1 rounded text-slate-600">${props.time}</span>
          <span class="text-[9px] font-bold truncate text-slate-700">${arg.event.title}</span>
        </div>
        <div class="text-[8px] text-slate-500 truncate px-0.5">
          ${props.species ? props.species + ' - ' : ''}${props.serviceType}
        </div>
      </div>
    `
  };
}

// COMPUTED: Métricas
const metrics = computed(() => {
  const todayStr = new Date().toISOString().split('T')[0];
  return {
    today: allEvents.value.filter(e => e.start.startsWith(todayStr)).length,
    pending: allEvents.value.filter(e => e.extendedProps.status === 'pending').length,
    confirmed: allEvents.value.filter(e => e.extendedProps.status === 'confirmed').length
  };
});

// COMPUTED: Filtrado
const filteredList = computed(() => {
  let list = allEvents.value;

  if (selectedDate.value) {
    list = list.filter(e => e.start.startsWith(selectedDate.value));
  } else {
    const today = new Date().toISOString().split('T')[0];
    list = list.filter(e => e.start >= today).sort((a, b) => new Date(a.start) - new Date(b.start));
  }

  if (activeFilter.value !== 'all') {
    list = list.filter(e => e.extendedProps.status === activeFilter.value);
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    list = list.filter(e => 
      e.title.toLowerCase().includes(query) || 
      e.extendedProps.client.toLowerCase().includes(query) ||
      (e.extendedProps.pet && e.extendedProps.pet.toLowerCase().includes(query))
    );
  }

  return list.slice(0, 20); 
});

const fetchAppointments = async () => {
  try {
    const [appointmentsRes, requestsData] = await Promise.all([
      axios.get(`${import.meta.env.VITE_API_URL}/appointments/all`, { headers: { Authorization: `Bearer ${userStore.token}` } }),
      getAllRequests() // Fetch all requests to filter by date
    ]);

    // Map Appointments
    const appointmentEvents = appointmentsRes.data.map(app => ({
      id: `app-${app.id}`,
      title: app.pet_id ? `Mascota #${app.pet_id}` : 'Consulta',
      start: `${app.appointment_date}T${app.appointment_time}`,
      backgroundColor: getStatusColor(app.status),
      borderColor: 'transparent',
      textColor: '#475569', 
      classNames: ['compact-event'], 
      extendedProps: { 
        type: 'appointment',
        status: app.status, 
        statusLabel: app.status === 'confirmed' ? 'OK' : (app.status === 'pending' ? 'Pend.' : 'Canc.'),
        notes: app.notes, 
        client: `Cliente #${app.user_id}`, 
        pet: app.pet_id ? `ID: ${app.pet_id}` : 'Sin nombre',
        species: '', // Backend doesn't provide species for appointments yet
        serviceType: app.service_id || 'General',
        time: app.appointment_time.substring(0, 5) 
      }
    }));

    // Map Service Requests (Only those with preferredDate)
    const requestEvents = requestsData
      .filter(req => req.service_data && req.service_data.preferredDate)
      .map(req => {
        const timeMap = { 'morning': '09:00', 'afternoon': '14:00', 'evening': '18:00' };
        const time = timeMap[req.service_data.preferredTime] || '00:00';
        
        return {
          id: `req-${req.id}`,
          title: req.pet_name || req.service_data.petName || 'Solicitud',
          start: `${req.service_data.preferredDate.split('T')[0]}T${time}`,
          backgroundColor: req.service_data.isUrgent ? '#fee2e2' : '#e0f2fe', // Red tint for urgent, Blue for normal
          borderColor: 'transparent',
          textColor: '#475569',
          classNames: ['compact-event'],
          extendedProps: {
            type: 'request',
            status: req.status,
            statusLabel: req.service_data.isUrgent ? 'URGENTE' : (req.status === 'pending' ? 'Solicitud' : 'Rev.'),
            notes: req.service_data.symptoms || req.service_data.notes || req.service_data.description,
            client: req.user_name || `Cliente #${req.user_id}`,
            pet: req.pet_name || req.service_data.petName || 'Sin nombre',
            species: req.service_data.species || '',
            serviceType: req.service_type,
            time: req.service_data.preferredTime ? translateTimeSlot(req.service_data.preferredTime) : '??:??'
          }
        };
      });

    const combinedEvents = [...appointmentEvents, ...requestEvents];
    allEvents.value = combinedEvents;
    calendarOptions.value.events = combinedEvents;
  } catch (err) { console.error(err); }
};

const translateTimeSlot = (slot) => {
  const slots = { morning: 'Mañana', afternoon: 'Tarde', evening: 'Noche' };
  return slots[slot] || slot;
};

function getStatusColor(s) { 
  return s === 'confirmed' ? '#d1fae5' : s === 'pending' ? '#fef3c7' : '#fee2e2'; 
}

function getStatusBorder(s) {
  return s === 'confirmed' ? 'bg-emerald-500' : s === 'pending' ? 'bg-amber-500' : 'bg-rose-500';
}

function handleDateClick(info) { selectedDate.value = info.dateStr; }
function handleEventClick(info) {
  const props = info.event.extendedProps;
  selectedEvent.value = { 
    id: info.event.id, 
    title: info.event.title, 
    start: info.event.startStr, 
    client: props.client, 
    pet: props.pet, 
    notes: props.notes,
    time: props.time,
    statusLabel: props.statusLabel,
  };
  isModalOpen.value = true;
}
function closeModal() { isModalOpen.value = false; }
function formatDateHeader(d) { return new Date(d + 'T00:00:00').toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'short' }); }
const formatFullDate = (d) => new Date(d).toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long' });

onMounted(() => { fetchAppointments(); });
</script>

<style>
/* ESTILOS FINOS */
.micro-calendar { font-size: 11px; --fc-border-color: #f1f5f9; --fc-today-bg-color: #f8fafc; }
.fc .fc-toolbar-title { font-size: 0.9rem; font-weight: 800; color: #334155; text-transform: capitalize; }
.fc .fc-button { padding: 0.15rem 0.5rem; font-size: 0.7rem; background: white; border: 1px solid #e2e8f0; color: #64748b; border-radius: 6px; box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05); font-weight: 600; text-transform: capitalize; }
.fc .fc-button:hover { background: #f1f5f9; color: #0f172a; border-color: #cbd5e1; }
.fc .fc-button-active { background: #f8fafc !important; border-color: #94a3b8 !important; color: #0f172a !important; }
.fc-theme-standard th { border: none !important; padding-bottom: 8px !important; }
.fc-col-header-cell-cushion { font-size: 0.65rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; }
.fc-daygrid-day-frame { min-height: 40px !important; }
.fc-daygrid-day-number { font-size: 0.7rem; color: #64748b; font-weight: 500; padding: 4px !important; }
.compact-event { margin-top: 2px; border-radius: 4px; font-size: 9px; font-weight: 600; padding: 2px; border: none !important; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>