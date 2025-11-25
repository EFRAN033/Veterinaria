<template>
  <div class="min-h-screen bg-gray-50 py-8 px-4 sm:px-6 lg:px-8 font-sans">
    
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900 tracking-tight">Agenda Veterinaria</h2>
      <p class="text-sm text-gray-500">Gestión de turnos y disponibilidad.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
      
      <div class="lg:col-span-8 xl:col-span-9">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden h-full">
          <div class="p-4">
            <FullCalendar :options="calendarOptions" class="custom-calendar" />
          </div>
        </div>
      </div>

      <div class="lg:col-span-4 xl:col-span-3 flex flex-col gap-6">
        
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 flex-1 flex flex-col overflow-hidden">
          <div class="p-4 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
            <h3 class="font-semibold text-gray-900">
              {{ selectedDate ? formatDateHeader(selectedDate) : 'Próximas Citas' }}
            </h3>
            <span class="text-xs font-medium px-2 py-1 bg-white rounded border border-gray-200 text-gray-500">
              {{ activeAppointments.length }} eventos
            </span>
          </div>

          <div class="p-4 overflow-y-auto max-h-[600px] space-y-3 custom-scrollbar">
            <div v-if="activeAppointments.length === 0" class="text-center py-10">
              <CalendarIcon class="h-12 w-12 text-gray-300 mx-auto mb-2" />
              <p class="text-sm text-gray-500">No hay citas para este periodo.</p>
            </div>

            <div 
              v-for="app in activeAppointments" 
              :key="app.id" 
              class="group relative bg-white p-3 rounded-lg border border-gray-100 hover:border-indigo-300 hover:shadow-md transition-all cursor-pointer"
              @click="openDetails(app)"
            >
              <div class="flex items-start justify-between">
                <div class="flex flex-col">
                  <span class="text-xs font-bold text-indigo-600 uppercase tracking-wider mb-1">
                    {{ app.extendedProps.time }}
                  </span>
                  <h4 class="text-sm font-semibold text-gray-900">{{ app.title }}</h4>
                  <p class="text-xs text-gray-500 mt-1 flex items-center gap-1">
                    <UserIcon class="h-3 w-3" /> {{ app.extendedProps.client }}
                  </p>
                </div>
                <span class="h-2.5 w-2.5 rounded-full flex-shrink-0 mt-1" :style="{ backgroundColor: app.backgroundColor }"></span>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
          <h4 class="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-3">Referencia</h4>
          <div class="space-y-2">
            <div class="flex items-center text-sm text-gray-600"><span class="w-2 h-2 rounded-full bg-emerald-500 mr-2"></span> Confirmada</div>
            <div class="flex items-center text-sm text-gray-600"><span class="w-2 h-2 rounded-full bg-amber-500 mr-2"></span> Pendiente</div>
            <div class="flex items-center text-sm text-gray-600"><span class="w-2 h-2 rounded-full bg-rose-500 mr-2"></span> Cancelada</div>
          </div>
        </div>

      </div>
    </div>

    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/50 backdrop-blur-sm" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden transform transition-all scale-100">
        <div class="bg-indigo-600 px-4 py-3 flex justify-between items-center">
          <h3 class="text-white font-semibold">Detalles de Cita #{{ selectedEvent.id }}</h3>
          <button @click="closeModal" class="text-white/80 hover:text-white"><XMarkIcon class="h-5 w-5"/></button>
        </div>
        <div class="p-6 space-y-4">
          <div class="flex items-center gap-3">
            <div class="p-2 bg-indigo-50 rounded-lg text-indigo-600"><ClockIcon class="h-6 w-6"/></div>
            <div>
              <p class="text-sm text-gray-500">Horario</p>
              <p class="font-medium text-gray-900">{{ formatFullDate(selectedEvent.start) }}</p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <div class="p-2 bg-purple-50 rounded-lg text-purple-600"><UserIcon class="h-6 w-6"/></div>
            <div>
              <p class="text-sm text-gray-500">Cliente / Paciente</p>
              <p class="font-medium text-gray-900">{{ selectedEvent.client }} / {{ selectedEvent.pet }}</p>
            </div>
          </div>
          <div class="mt-4 pt-4 border-t border-gray-100">
            <p class="text-sm text-gray-500 mb-1">Notas del servicio:</p>
            <p class="text-sm text-gray-700 italic bg-gray-50 p-3 rounded">{{ selectedEvent.notes || 'Sin notas' }}</p>
          </div>
        </div>
        <div class="px-4 py-3 bg-gray-50 text-right">
          <button @click="closeModal" class="text-sm font-medium text-gray-600 hover:text-gray-900">Cerrar</button>
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
import timeGridPlugin from '@fullcalendar/timegrid';
import listPlugin from '@fullcalendar/list';
import esLocale from '@fullcalendar/core/locales/es';
import axios from 'axios';
import { useUserStore } from '@/stores/user';
import { 
  CalendarIcon, 
  UserIcon, 
  ClockIcon, 
  XMarkIcon 
} from '@heroicons/vue/24/outline';

const userStore = useUserStore();
const isModalOpen = ref(false);
const selectedEvent = ref({});
const selectedDate = ref(null); 
const allEvents = ref([]); 

const calendarOptions = ref({
  plugins: [dayGridPlugin, interactionPlugin, timeGridPlugin, listPlugin],
  initialView: 'dayGridMonth',
  locale: esLocale,
  height: 'auto',
  contentHeight: 600,
  headerToolbar: {
    left: 'prev,next title',
    center: '',
    right: 'dayGridMonth,timeGridWeek'
  },
  buttonText: {
    today: 'Hoy',
    month: 'Mes',
    week: 'Semana',
  },
  events: [],
  dateClick: handleDateClick,
  eventClick: handleEventClick,
  editable: false,
  dayMaxEvents: 2, 
  fixedWeekCount: false,
});

const activeAppointments = computed(() => {
  if (selectedDate.value) {
    return allEvents.value.filter(event => {
      return event.start.startsWith(selectedDate.value); 
    });
  }
  const today = new Date().toISOString().split('T')[0];
  return allEvents.value
    .filter(e => e.start >= today)
    .sort((a, b) => new Date(a.start) - new Date(b.start))
    .slice(0, 6);
});

const fetchAppointments = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/appointments/all', {
      headers: { Authorization: `Bearer ${userStore.token}` }
    });
    
    const mappedEvents = response.data.map(app => {
      const styles = getStatusStyles(app.status);
      return {
        id: app.id,
        title: app.service_id || `Cita #${app.id}`,
        start: `${app.appointment_date}T${app.appointment_time}`,
        backgroundColor: styles.bg,
        borderColor: 'transparent',
        textColor: styles.text,
        extendedProps: {
          status: app.status,
          notes: app.notes,
          client: app.user_id,
          pet: app.pet_id,
          time: app.appointment_time.substring(0, 5) 
        }
      };
    });

    allEvents.value = mappedEvents;
    calendarOptions.value.events = mappedEvents;

  } catch (err) {
    console.error('Error fetching calendar events:', err);
  }
};

function getStatusStyles(status) {
  switch(status) {
    case 'confirmed': return { bg: '#10B981', text: '#FFFFFF' };
    case 'pending': return { bg: '#F59E0B', text: '#FFFFFF' };
    case 'cancelled': return { bg: '#EF4444', text: '#FFFFFF' };
    default: return { bg: '#6B7280', text: '#FFFFFF' };
  }
}

function handleDateClick(info) {
  selectedDate.value = info.dateStr; 
}

function handleEventClick(info) {
  openDetails({
    id: info.event.id,
    title: info.event.title,
    start: info.event.startStr || info.event.start.toISOString(),
    backgroundColor: info.event.backgroundColor,
    extendedProps: info.event.extendedProps
  });
}

function openDetails(eventData) {
  selectedEvent.value = {
    id: eventData.id,
    title: eventData.title,
    start: eventData.start,
    client: eventData.extendedProps.client,
    pet: eventData.extendedProps.pet || 'N/A',
    notes: eventData.extendedProps.notes,
    color: eventData.backgroundColor
  };
  isModalOpen.value = true;
}

function closeModal() {
  isModalOpen.value = false;
}

function formatDateHeader(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long' });
}

const formatFullDate = (date) => {
  if (!date) return '';
  return new Date(date).toLocaleDateString('es-ES', {
    weekday: 'short', year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });
};

onMounted(() => {
  fetchAppointments();
});
</script>

<style>
.custom-calendar {
  font-size: 0.85rem; 
}

.fc .fc-toolbar-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1f2937;
}

.fc .fc-button {
  font-size: 0.75rem;
  padding: 0.25rem 0.6rem;
  font-weight: 500;
}

.fc-col-header-cell-cushion {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: #6b7280;
  font-weight: 600;
  padding-bottom: 8px !important;
}

.fc-daygrid-day-frame {
  min-height: 80px !important;
}

.fc-daygrid-day-number {
  font-size: 0.8rem;
  color: #374151;
  padding: 4px !important;
}

.fc-event {
  border-radius: 4px;
  padding: 1px 3px;
  font-size: 0.7rem;
  border: none;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f1f1; 
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d1d5db; 
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #9ca3af; 
}
</style>