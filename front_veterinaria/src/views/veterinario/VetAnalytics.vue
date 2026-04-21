<template>
  <div class="h-full flex flex-col font-sans text-slate-600">
    <div class="mb-6 shrink-0">
      <h2 class="text-xl font-bold text-slate-800 flex items-center gap-2">
        <ChartBarIcon class="h-7 w-7 text-[#02939E]" />
        Análisis
      </h2>
      <p class="text-sm text-slate-500 mt-1">
        Métricas de citas con filtros por especie y sexo. Los datos respetan el rango de meses seleccionado.
      </p>
    </div>

    <div class="flex flex-wrap items-end gap-4 mb-6 bg-white border border-slate-200 p-4 rounded-none shadow-sm">
      <div>
        <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Especie</label>
        <select
          v-model="filters.species"
          class="border border-slate-200 rounded-none px-3 py-2 text-sm min-w-[140px] focus:border-[#02939E] focus:ring-1 focus:ring-[#02939E]/30"
        >
          <option value="">Todas</option>
          <option value="perro">Perro</option>
          <option value="gato">Gato</option>
        </select>
      </div>
      <div>
        <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Sexo</label>
        <select
          v-model="filters.sex"
          class="border border-slate-200 rounded-none px-3 py-2 text-sm min-w-[140px] focus:border-[#02939E] focus:ring-1 focus:ring-[#02939E]/30"
        >
          <option value="">Todos</option>
          <option value="macho">Macho</option>
          <option value="hembra">Hembra</option>
        </select>
      </div>
      <div>
        <label class="block text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">Rango (meses)</label>
        <select
          v-model.number="filters.rangeMonths"
          class="border border-slate-200 rounded-none px-3 py-2 text-sm min-w-[100px] focus:border-[#02939E] focus:ring-1 focus:ring-[#02939E]/30"
        >
          <option :value="6">6</option>
          <option :value="12">12</option>
          <option :value="24">24</option>
        </select>
      </div>
      <button
        type="button"
        class="px-5 py-2 bg-[#02939E] text-white text-sm font-bold rounded-none hover:bg-[#027a83] transition-colors"
        :disabled="loading"
        @click="load"
      >
        {{ loading ? 'Cargando…' : 'Aplicar' }}
      </button>
    </div>

    <p v-if="error" class="text-sm text-rose-600 mb-4">{{ error }}</p>

    <div v-if="loading && !analytics" class="flex-1 flex items-center justify-center py-20 text-slate-400 text-sm">
      Cargando analíticas…
    </div>

    <div v-else-if="analytics" class="grid grid-cols-1 lg:grid-cols-2 gap-6 flex-1 min-h-0">
      <div class="bg-white border border-slate-200 p-5 rounded-none shadow-sm">
        <h3 class="text-sm font-bold text-slate-800 mb-4">Resumen</h3>
        <dl class="space-y-3 text-sm">
          <div class="flex justify-between border-b border-slate-100 pb-2">
            <dt class="text-slate-500">Citas en el período</dt>
            <dd class="font-bold text-[#02939E]">{{ analytics.total_appointments }}</dd>
          </div>
          <div class="flex justify-between border-b border-slate-100 pb-2">
            <dt class="text-slate-500">Mascotas distintas atendidas</dt>
            <dd class="font-bold text-slate-800">{{ analytics.unique_pets_attended }}</dd>
          </div>
          <div class="flex justify-between border-b border-slate-100 pb-2">
            <dt class="text-slate-500">Seguimiento (cita futura)</dt>
            <dd class="font-bold text-slate-800">{{ analytics.follow_up_patients_count }}</dd>
          </div>
        </dl>
        <p class="text-[11px] text-slate-400 mt-4 leading-relaxed">
          {{ analytics.follow_up_legend }}
        </p>
      </div>

      <div class="bg-white border border-slate-200 p-5 rounded-none shadow-sm">
        <h3 class="text-sm font-bold text-slate-800 mb-4">Citas por estado</h3>
        <div v-if="!analytics.appointments_by_status?.length" class="text-xs text-slate-400">Sin datos.</div>
        <table v-else class="w-full text-xs">
          <thead>
            <tr class="text-left text-slate-400 border-b border-slate-100">
              <th class="pb-2 font-bold uppercase tracking-wider">Estado</th>
              <th class="pb-2 font-bold uppercase tracking-wider text-right">Cantidad</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in analytics.appointments_by_status" :key="row.status" class="border-b border-slate-50">
              <td class="py-2 capitalize">{{ row.status }}</td>
              <td class="py-2 text-right font-mono font-medium">{{ row.count }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="lg:col-span-2 bg-white border border-slate-200 p-5 rounded-none shadow-sm">
        <h3 class="text-sm font-bold text-slate-800 mb-4">Citas por mes</h3>
        <div v-if="!analytics.appointments_by_month?.length" class="text-xs text-slate-400">Sin datos en el rango.</div>
        <div v-else class="space-y-3">
          <div v-for="row in chartRows" :key="row.month" class="flex items-center gap-3">
            <span class="w-24 shrink-0 text-[11px] font-mono text-slate-500">{{ row.label }}</span>
            <div class="flex-1 h-7 bg-slate-100 rounded-none overflow-hidden">
              <div
                class="h-full bg-[#02939E] transition-all duration-500 rounded-none"
                :style="{ width: row.pct + '%' }"
              />
            </div>
            <span class="w-10 text-right text-xs font-bold text-slate-700">{{ row.count }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { ChartBarIcon } from '@heroicons/vue/24/outline';
import apiClient from '@/axios';

const loading = ref(false);
const error = ref(null);
const analytics = ref(null);

const filters = ref({
  species: '',
  sex: '',
  rangeMonths: 12,
});

const chartRows = computed(() => {
  const rows = analytics.value?.appointments_by_month || [];
  const max = Math.max(...rows.map((r) => r.count), 1);
  return rows.map((r) => ({
    month: r.month,
    count: r.count,
    pct: Math.round((r.count / max) * 100),
    label: formatMonthLabel(r.month),
  }));
});

function formatMonthLabel(iso) {
  if (!iso) return '';
  const d = new Date(iso + 'T12:00:00');
  return d.toLocaleDateString('es-ES', { month: 'short', year: 'numeric' });
}

async function load() {
  loading.value = true;
  error.value = null;
  try {
    const params = { range_months: filters.value.rangeMonths };
    if (filters.value.species) params.species = filters.value.species;
    if (filters.value.sex) params.sex = filters.value.sex;
    const { data } = await apiClient.get('/v1/vet/analytics', { params });
    analytics.value = data;
  } catch (e) {
    console.error(e);
    error.value = 'No se pudieron cargar las analíticas. Verifica tu sesión.';
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  load();
});
</script>
