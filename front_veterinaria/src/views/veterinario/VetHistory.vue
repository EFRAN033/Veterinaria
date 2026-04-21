<template>
  <div class="h-full flex flex-col font-sans text-slate-600 bg-slate-50/50">
    <div class="mb-6 shrink-0 px-1">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <h2 class="app-type-toolbar-title flex items-center gap-2">
            <ClipboardDocumentListIcon class="h-7 w-7 text-[#02939E]" />
            Historial Clínico
          </h2>
          <p class="text-sm text-slate-500 mt-1">
            Citas de todas las mascotas y solicitudes revisadas. Diagnóstico final y tratamiento por cita (solo citas).
          </p>
        </div>

        <div class="flex items-center gap-3 bg-white p-1.5 rounded-none border border-slate-200 shadow-sm">
          <div class="relative group">
            <input
              v-model="searchTerm"
              type="text"
              placeholder="Buscar paciente, especie, notas…"
              class="pl-9 pr-4 py-2 text-xs font-medium bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:border-[#02939E] focus:ring-2 focus:ring-[#02939E]/15 text-slate-600 w-64 transition-all group-hover:bg-white"
            />
            <MagnifyingGlassIcon class="h-4 w-4 text-slate-400 absolute left-3 top-2.5 group-hover:text-[#02939E] transition-colors" />
          </div>
          <div class="px-3 py-2 bg-slate-100 rounded-lg border border-slate-200 flex flex-col items-center justify-center min-w-[60px]">
            <span class="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Total</span>
            <span class="text-xs font-bold text-slate-700">{{ filteredRecords.length }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="flex-1 bg-white rounded-none shadow-[0_-4px_20px_rgba(0,0,0,0.02)] border border-slate-200 overflow-hidden flex flex-col min-h-0">
      <div
        class="grid grid-cols-12 gap-2 px-4 py-4 border-b border-slate-100 bg-slate-50/50 text-[10px] font-bold text-slate-400 uppercase tracking-wider shrink-0"
      >
        <div class="col-span-2">Fecha / Hora</div>
        <div class="col-span-2">Tipo</div>
        <div class="col-span-2">Paciente</div>
        <div class="col-span-1">Estado</div>
        <div class="col-span-2">Notas</div>
        <div class="col-span-2">Clínico</div>
        <div class="col-span-1 text-right">Acciones</div>
      </div>

      <div v-if="loading" class="flex-1 flex flex-col items-center justify-center space-y-3">
        <LoadingSpinner />
        <p class="text-xs font-medium text-slate-400 animate-pulse">Cargando expediente…</p>
      </div>

      <div v-else class="flex-1 overflow-y-auto custom-scrollbar p-2">
        <div v-if="filteredRecords.length === 0" class="h-full flex flex-col items-center justify-center text-slate-400 opacity-60 py-16">
          <ArchiveBoxXMarkIcon class="h-16 w-16 mb-4 text-slate-200" />
          <p class="text-sm font-medium">No se encontraron registros</p>
          <p class="text-xs mt-1">Intenta con otro término de búsqueda.</p>
        </div>

        <template v-for="record in filteredRecords" :key="record.type + '-' + record.id">
          <div
            class="group grid grid-cols-12 gap-2 items-start px-3 py-3 mb-2 rounded-none hover:bg-slate-50 transition-all duration-200 border border-transparent hover:border-slate-100 relative overflow-hidden"
          >
            <div class="absolute left-0 top-2 bottom-2 w-1 rounded-r-full" :class="getStatusBorder(record.status)"></div>

            <div class="col-span-2 pl-2">
              <div class="flex items-center gap-2">
                <div
                  class="flex flex-col items-center justify-center w-9 h-9 rounded-lg border bg-white shadow-sm shrink-0"
                  :class="getDateBoxColor(record.status)"
                >
                  <span class="text-[8px] uppercase font-bold opacity-60">{{ getDayName(record.date) }}</span>
                  <span class="text-xs font-black leading-none">{{ getDayNumber(record.date) }}</span>
                </div>
                <div class="flex flex-col min-w-0">
                  <span class="text-[9px] uppercase font-bold text-slate-400 truncate">{{ getMonthYear(record.date) }}</span>
                  <span class="text-[11px] font-mono font-medium text-slate-600">{{ record.time || '--:--' }}</span>
                </div>
              </div>
            </div>

            <div class="col-span-2">
              <span
                class="inline-flex items-center gap-1 px-2 py-1 rounded-lg text-[10px] font-bold uppercase"
                :class="getTypeClass(record.type)"
              >
                {{ getTypeLabel(record.type) }}
              </span>
            </div>

            <div class="col-span-2 min-w-0">
              <div class="flex items-center gap-1 mb-0.5">
                <UserIcon class="h-3 w-3 text-slate-400 shrink-0" />
                <span class="text-xs font-bold text-slate-700 truncate">{{ record.patientName }}</span>
              </div>
              <p v-if="record.type === 'appointment'" class="text-[10px] text-slate-500 truncate">
                <span v-if="record.species">{{ record.species }}</span>
                <span v-if="record.gender"> · {{ record.gender }}</span>
                <span v-if="record.petId"> · ID {{ record.petId }}</span>
              </p>
            </div>

            <div class="col-span-1">
              <span
                class="inline-flex items-center gap-1 px-1.5 py-0.5 rounded-full text-[9px] font-bold uppercase tracking-wide border"
                :class="getStatusBadge(record.status)"
              >
                <span class="w-1 h-1 rounded-full shrink-0" :class="getStatusDot(record.status)"></span>
                <span class="truncate">{{ getStatusLabel(record.status) }}</span>
              </span>
            </div>

            <div class="col-span-2 min-w-0">
              <p v-if="record.notes" class="text-[11px] text-slate-600 leading-snug line-clamp-2 italic">
                {{ record.notes }}
              </p>
              <span v-else class="text-[10px] text-slate-300 font-bold">—</span>
            </div>

            <div class="col-span-2 min-w-0">
              <template v-if="record.type === 'appointment'">
                <p class="text-[10px] text-slate-500 line-clamp-1">
                  <span class="font-bold text-slate-600">Dx:</span>
                  {{ record.finalDiagnosis || '—' }}
                </p>
                <p class="text-[10px] text-slate-500 line-clamp-1 mt-0.5">
                  <span class="font-bold text-slate-600">Tr:</span>
                  {{ record.treatment || '—' }}
                </p>
              </template>
              <span v-else class="text-[10px] text-slate-300">—</span>
            </div>

            <div class="col-span-1 flex flex-col items-end gap-1">
              <span class="text-[9px] font-mono text-slate-300">#{{ record.id }}</span>
              <button
                v-if="record.type === 'appointment'"
                type="button"
                class="text-[10px] font-bold text-[#02939E] hover:underline"
                @click="toggleClinical(record)"
              >
                {{ expandedId === record.id ? 'Cerrar' : 'Editar' }}
              </button>
            </div>
          </div>

          <div
            v-if="record.type === 'appointment' && expandedId === record.id"
            class="mx-2 mb-4 px-4 py-4 bg-slate-50 border border-slate-200 rounded-none"
          >
            <p class="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-3">Registro clínico (cita #{{ record.id }})</p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-[10px] font-bold text-slate-400 mb-1">Diagnóstico final</label>
                <textarea
                  v-model="drafts[record.id].final_diagnosis"
                  rows="4"
                  class="w-full text-xs border border-slate-200 rounded-none p-2 focus:border-[#02939E] focus:ring-1 focus:ring-[#02939E]/20"
                  placeholder="Diagnóstico confirmado…"
                />
              </div>
              <div>
                <label class="block text-[10px] font-bold text-slate-400 mb-1">Tratamiento</label>
                <textarea
                  v-model="drafts[record.id].treatment"
                  rows="4"
                  class="w-full text-xs border border-slate-200 rounded-none p-2 focus:border-[#02939E] focus:ring-1 focus:ring-[#02939E]/20"
                  placeholder="Medicación, indicaciones…"
                />
              </div>
            </div>
            <div class="mt-3 flex justify-end gap-2">
              <button
                type="button"
                class="px-3 py-1.5 text-xs font-medium text-slate-600 border border-slate-200 rounded-none hover:bg-white"
                @click="expandedId = null"
              >
                Cancelar
              </button>
              <button
                type="button"
                class="px-4 py-1.5 text-xs font-bold bg-[#02939E] text-white rounded-none hover:bg-[#027a83] disabled:opacity-50"
                :disabled="savingId === record.id"
                @click="saveClinical(record)"
              >
                {{ savingId === record.id ? 'Guardando…' : 'Guardar' }}
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue';
import { useServiceRequests } from '@/composables/useServiceRequests';
import apiClient from '@/axios';
import LoadingSpinner from '@/components/LoadingSpinner.vue';
import {
  MagnifyingGlassIcon,
  ClipboardDocumentListIcon,
  UserIcon,
  ArchiveBoxXMarkIcon,
} from '@heroicons/vue/24/outline';

const appointments = ref([]);
const serviceRequests = ref([]);
const loading = ref(true);
const searchTerm = ref('');
const { getAllRequests } = useServiceRequests();

const expandedId = ref(null);
const savingId = ref(null);
const drafts = reactive({});

const getDayName = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('es-ES', { weekday: 'short' }).substring(0, 3);
};
const getDayNumber = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.getDate();
};
const getMonthYear = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('es-ES', { month: 'short', year: '2-digit' });
};

const getTypeClass = (type) => {
  if (type === 'appointment') return 'bg-[#02939E]/10 text-[#027a83] border border-[#02939E]/20';
  if (type === 'service_request') return 'bg-[#02939E]/12 text-[#027a83] border border-[#02939E]/25';
  return 'bg-slate-100 text-slate-600';
};

const getTypeLabel = (type) => {
  if (type === 'appointment') return 'Cita';
  if (type === 'service_request') return 'Solicitud';
  return type;
};

const getStatusBorder = (status) => {
  if (status === 'completed' || status === 'reviewed') return 'bg-[#02939E]';
  if (status === 'cancelled') return 'bg-rose-500';
  return 'bg-slate-300';
};

const getDateBoxColor = (status) => {
  if (status === 'completed' || status === 'reviewed') return 'border-[#02939E]/35 text-[#02939E]';
  if (status === 'cancelled') return 'border-rose-200 text-rose-700 opacity-75';
  return 'border-slate-200 text-slate-500';
};

const getStatusBadge = (status) => {
  if (status === 'completed' || status === 'reviewed') return 'bg-[#02939E]/10 text-[#027a83] border-[#02939E]/20';
  if (status === 'cancelled') return 'bg-rose-50 text-rose-700 border-rose-100';
  return 'bg-slate-100 text-slate-600 border-slate-200';
};

const getStatusDot = (status) => {
  if (status === 'completed' || status === 'reviewed') return 'bg-[#02939E]';
  if (status === 'cancelled') return 'bg-rose-500';
  return 'bg-slate-400';
};

const getStatusLabel = (status) => {
  if (status === 'completed') return 'Completada';
  if (status === 'cancelled') return 'Cancelada';
  if (status === 'reviewed') return 'Revisada';
  if (status === 'pending') return 'Pendiente';
  if (status === 'confirmed') return 'Confirmada';
  return status;
};

function toggleClinical(record) {
  if (expandedId.value === record.id) {
    expandedId.value = null;
    return;
  }
  expandedId.value = record.id;
  if (!drafts[record.id]) {
    drafts[record.id] = {
      final_diagnosis: record.finalDiagnosis || '',
      treatment: record.treatment || '',
    };
  }
}

async function saveClinical(record) {
  savingId.value = record.id;
  try {
    const body = {
      final_diagnosis: drafts[record.id].final_diagnosis,
      treatment: drafts[record.id].treatment,
    };
    await apiClient.patch(`/v1/appointments/${record.id}/clinical`, body);
    const app = appointments.value.find((a) => a.id === record.id);
    if (app) {
      app.final_diagnosis = body.final_diagnosis;
      app.treatment = body.treatment;
    }
    expandedId.value = null;
  } catch (e) {
    console.error(e);
    alert('No se pudo guardar el registro clínico.');
  } finally {
    savingId.value = null;
  }
}

const fetchHistory = async () => {
  loading.value = true;
  try {
    const appointmentsResponse = await apiClient.get('/v1/appointments/vet/history', {
      params: { limit: 500 },
    });
    appointments.value = appointmentsResponse.data;

    const reviewedRequests = await getAllRequests({ status: 'reviewed' });
    serviceRequests.value = reviewedRequests;
  } catch (err) {
    console.error('Error fetching history:', err);
  } finally {
    loading.value = false;
  }
};

const allRecords = computed(() => {
  const appointmentRecords = appointments.value.map((app) => ({
    id: app.id,
    type: 'appointment',
    date: app.appointment_date,
    time: app.appointment_time?.substring?.(0, 5) || app.appointment_time,
    patientName: app.pet_name || `Cliente ${app.user_id}`,
    petId: app.pet_id,
    species: app.species,
    gender: app.gender,
    status: app.status,
    notes: app.notes,
    finalDiagnosis: app.final_diagnosis,
    treatment: app.treatment,
  }));

  const serviceRequestRecords = serviceRequests.value.map((req) => ({
    id: req.id,
    type: 'service_request',
    date: req.created_at.split('T')[0],
    time: req.created_at.split('T')[1]?.substring(0, 5),
    patientName: req.pet_name || `Cliente ${req.user_id}`,
    petId: null,
    species: null,
    gender: null,
    status: req.status,
    notes:
      req.vet_notes ||
      (req.service_data?.symptoms ? `Síntomas: ${req.service_data.symptoms.substring(0, 100)}` : null),
    finalDiagnosis: null,
    treatment: null,
  }));

  return [...appointmentRecords, ...serviceRequestRecords].sort((a, b) => {
    return new Date(b.date + ' ' + (b.time || '00:00')) - new Date(a.date + ' ' + (a.time || '00:00'));
  });
});

const filteredRecords = computed(() => {
  const term = searchTerm.value.toLowerCase();
  if (!term) return allRecords.value;
  return allRecords.value.filter(
    (record) =>
      record.id.toString().includes(term) ||
      record.status.toLowerCase().includes(term) ||
      record.patientName.toLowerCase().includes(term) ||
      (record.notes && record.notes.toLowerCase().includes(term)) ||
      (record.species && record.species.toLowerCase().includes(term)) ||
      (record.gender && record.gender.toLowerCase().includes(term)) ||
      (record.finalDiagnosis && record.finalDiagnosis.toLowerCase().includes(term)) ||
      (record.treatment && record.treatment.toLowerCase().includes(term)),
  );
});

onMounted(() => {
  fetchHistory();
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
