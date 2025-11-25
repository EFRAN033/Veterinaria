<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="text-center">
      <h3 class="text-2xl font-serif font-bold text-gray-900">¿Cuándo prefieres la atención?</h3>
      <p class="text-gray-500 mt-2">Selecciona la fecha y hora que mejor se adapte a ti.</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
      <!-- Calendar Section -->
      <div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm">
        <div class="flex items-center justify-between mb-6">
          <button @click="prevMonth" class="p-2 hover:bg-gray-50 rounded-full text-gray-400 hover:text-[#1BB0B9] transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" /></svg>
          </button>
          <h4 class="font-bold text-gray-800 capitalize">{{ currentMonthName }} {{ currentYear }}</h4>
          <button @click="nextMonth" class="p-2 hover:bg-gray-50 rounded-full text-gray-400 hover:text-[#1BB0B9] transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
          </button>
        </div>

        <!-- Weekdays -->
        <div class="grid grid-cols-7 mb-4">
          <div v-for="day in weekDays" :key="day" class="text-center text-xs font-bold text-gray-400 uppercase tracking-wider py-2">
            {{ day }}
          </div>
        </div>

        <!-- Days -->
        <div class="grid grid-cols-7 gap-2">
          <div v-for="{ date, isCurrentMonth, isToday, isPast, isSelected } in calendarDays" :key="date.toISOString()" class="aspect-square">
            <button 
              @click="selectDate(date)"
              :disabled="isPast"
              class="w-full h-full rounded-xl flex items-center justify-center text-sm font-medium transition-all duration-200 relative group"
              :class="[
                isSelected ? 'bg-[#1BB0B9] text-white shadow-lg shadow-[#1BB0B9]/30' : 
                isPast ? 'text-gray-300 cursor-not-allowed' : 
                isCurrentMonth ? 'text-gray-700 hover:bg-[#1BB0B9]/10 hover:text-[#1BB0B9]' : 'text-gray-300'
              ]"
            >
              {{ date.getDate() }}
              <span v-if="isToday && !isSelected" class="absolute bottom-1.5 left-1/2 -translate-x-1/2 w-1 h-1 rounded-full bg-[#1BB0B9]"></span>
            </button>
          </div>
        </div>
      </div>

      <!-- Time Selection & Urgency -->
      <div class="space-y-8">
        <!-- Urgency Toggle -->
        <div class="bg-[#FFF8F6] border border-[#FFDDD6] rounded-2xl p-4 flex items-start gap-4 cursor-pointer hover:bg-[#FFF0EB] transition-colors" @click="toggleUrgency">
          <div class="bg-white p-2 rounded-xl text-[#FF6B6B] shadow-sm shrink-0">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <div class="flex-1">
            <div class="flex items-center justify-between">
              <h4 class="font-bold text-[#FF6B6B]">Lo antes posible</h4>
              <div class="w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors"
                :class="modelValue.isUrgent ? 'border-[#FF6B6B] bg-[#FF6B6B]' : 'border-[#FFDDD6] bg-white'">
                <svg v-if="modelValue.isUrgent" class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg>
              </div>
            </div>
            <p class="text-sm text-[#FF6B6B]/80 mt-1">Selecciona esto si es una emergencia. Nos pondremos en contacto de inmediato.</p>
          </div>
        </div>

        <!-- Time Slots -->
        <div class="space-y-4" :class="{ 'opacity-50 pointer-events-none': modelValue.isUrgent }">
          <h4 class="font-bold text-gray-900 flex items-center gap-2">
            <svg class="w-5 h-5 text-[#1BB0B9]" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            Horarios Disponibles
          </h4>
          
          <div class="grid grid-cols-1 gap-3">
            <button 
              v-for="slot in timeSlots" 
              :key="slot.id"
              @click="selectTime(slot.id)"
              class="flex items-center justify-between p-4 rounded-xl border-2 transition-all duration-200 group"
              :class="modelValue.timeSlot === slot.id 
                ? 'border-[#1BB0B9] bg-[#1BB0B9]/5' 
                : 'border-gray-100 bg-white hover:border-[#1BB0B9]/30'"
            >
              <div class="flex items-center gap-3">
                <div class="p-2 rounded-lg" :class="modelValue.timeSlot === slot.id ? 'bg-[#1BB0B9] text-white' : 'bg-gray-100 text-gray-400 group-hover:bg-[#1BB0B9]/10 group-hover:text-[#1BB0B9]'">
                  <component :is="slot.icon" class="w-5 h-5" />
                </div>
                <div class="text-left">
                  <span class="block font-bold text-sm" :class="modelValue.timeSlot === slot.id ? 'text-[#1BB0B9]' : 'text-gray-700'">{{ slot.label }}</span>
                  <span class="text-xs text-gray-400">{{ slot.hours }}</span>
                </div>
              </div>
              <div class="w-5 h-5 rounded-full border-2 flex items-center justify-center transition-colors"
                :class="modelValue.timeSlot === slot.id ? 'border-[#1BB0B9] bg-[#1BB0B9]' : 'border-gray-200'">
                <svg v-if="modelValue.timeSlot === slot.id" class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { SunIcon, MoonIcon, CloudIcon } from '@heroicons/vue/24/outline';

const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
    default: () => ({ date: null, timeSlot: '', isUrgent: false })
  }
});

const emit = defineEmits(['update:modelValue']);

const weekDays = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
const currentDate = ref(new Date());

const timeSlots = [
  { id: 'morning', label: 'Mañana', hours: '8:00 AM - 12:00 PM', icon: SunIcon },
  { id: 'afternoon', label: 'Tarde', hours: '12:00 PM - 5:00 PM', icon: CloudIcon },
  { id: 'evening', label: 'Noche', hours: '5:00 PM - 8:00 PM', icon: MoonIcon }
];

const currentMonthName = computed(() => {
  return currentDate.value.toLocaleString('es-ES', { month: 'long' });
});

const currentYear = computed(() => {
  return currentDate.value.getFullYear();
});

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();
  const firstDay = new Date(year, month, 1);
  const lastDay = new Date(year, month + 1, 0);
  
  const days = [];
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  // Previous month days
  const firstDayOfWeek = firstDay.getDay();
  for (let i = firstDayOfWeek; i > 0; i--) {
    const date = new Date(year, month, 1 - i);
    days.push(createDayObject(date, false, today));
  }

  // Current month days
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const date = new Date(year, month, i);
    days.push(createDayObject(date, true, today));
  }

  // Next month days to fill grid (42 days total for 6 rows)
  const remainingDays = 42 - days.length;
  for (let i = 1; i <= remainingDays; i++) {
    const date = new Date(year, month + 1, i);
    days.push(createDayObject(date, false, today));
  }

  return days;
});

const createDayObject = (date, isCurrentMonth, today) => {
  const isSelected = props.modelValue.date && 
    date.getDate() === props.modelValue.date.getDate() &&
    date.getMonth() === props.modelValue.date.getMonth() &&
    date.getFullYear() === props.modelValue.date.getFullYear();

  return {
    date,
    isCurrentMonth,
    isToday: date.getTime() === today.getTime(),
    isPast: date < today,
    isSelected
  };
};

const prevMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1);
};

const nextMonth = () => {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1);
};

const selectDate = (date) => {
  emit('update:modelValue', {
    ...props.modelValue,
    date: date,
    isUrgent: false
  });
};

const selectTime = (slotId) => {
  emit('update:modelValue', {
    ...props.modelValue,
    timeSlot: slotId,
    isUrgent: false
  });
};

const toggleUrgency = () => {
  const newValue = !props.modelValue.isUrgent;
  emit('update:modelValue', {
    ...props.modelValue,
    isUrgent: newValue,
    date: newValue ? null : props.modelValue.date,
    timeSlot: newValue ? '' : props.modelValue.timeSlot
  });
};

onMounted(() => {
  // Initialize with today if no date selected
  if (!props.modelValue.date) {
    // Optional: preselect today
  }
});
</script>
