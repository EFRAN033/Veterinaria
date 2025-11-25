<script setup>
import { ref, onMounted } from 'vue';
import FullCalendar from '@fullcalendar/vue3';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import axios from 'axios';
import { useUserStore } from '@/stores/user';

const userStore = useUserStore();
const calendarOptions = ref({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  headerToolbar: {
    left: 'prev,next today',
    center: 'title',
    right: 'dayGridMonth,dayGridWeek,dayGridDay'
  },
  events: [],
  eventClick: handleEventClick,
  locale: 'es',
  buttonText: {
    today: 'Hoy',
    month: 'Mes',
    week: 'Semana',
    day: 'Día'
  }
});

const fetchAppointments = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/appointments/all', {
      headers: { Authorization: `Bearer ${userStore.token}` }
    });
    
    calendarOptions.value.events = response.data.map(app => ({
      id: app.id,
      title: `Cita #${app.id} - ${app.status}`,
      start: `${app.appointment_date}T${app.appointment_time}`,
      backgroundColor: getStatusColor(app.status),
      borderColor: getStatusColor(app.status),
      extendedProps: {
        status: app.status,
        notes: app.notes
      }
    }));
  } catch (err) {
    console.error('Error fetching calendar events:', err);
  }
};

function getStatusColor(status) {
  switch(status) {
    case 'confirmed': return '#10B981'; // Green
    case 'pending': return '#F59E0B';   // Yellow
    case 'completed': return '#3B82F6'; // Blue
    case 'cancelled': return '#EF4444'; // Red
    default: return '#6B7280';          // Gray
  }
}

function handleEventClick(info) {
  alert(`Cita #${info.event.id}\nEstado: ${info.event.extendedProps.status}\nNotas: ${info.event.extendedProps.notes || 'Sin notas'}`);
}

onMounted(() => {
  fetchAppointments();
});
</script>

<template>
  <div class="bg-white p-6 rounded-lg shadow-md">
    <FullCalendar :options="calendarOptions" />
  </div>
</template>

<style>
/* Custom FullCalendar overrides if needed */
.fc-event {
  cursor: pointer;
}
</style>
