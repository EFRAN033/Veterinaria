<template>
  <div class="h-full flex flex-col bg-white border-l border-slate-200 w-80 shrink-0 overflow-hidden">
    
    <div class="p-4 bg-slate-50 border-b border-slate-100 shrink-0">
      <h3 class="font-bold text-slate-700 flex items-center gap-2">
        <LightBulbIcon class="h-5 w-5 text-amber-500" />
        Insights Clínicos
      </h3>
      <p class="text-[10px] text-slate-400 mt-1">Análisis en tiempo real de la IA.</p>
    </div>

    <div class="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-6">
      
      <!-- Differential Diagnosis -->
      <div v-if="insights?.differentials?.length" class="space-y-3 animate-fade-in">
        <label class="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
          <ChartPieIcon class="h-3 w-3" /> Diagnóstico Diferencial
        </label>
        
        <div class="space-y-3">
          <div v-for="(diff, idx) in insights.differentials" :key="idx" class="space-y-1">
            <div class="flex justify-between text-xs">
              <span class="font-bold text-slate-700">{{ diff.name }}</span>
              <span class="text-[10px] font-mono text-slate-400">{{ diff.probability }}</span>
            </div>
            <div class="h-1.5 bg-slate-100 rounded-full overflow-hidden">
              <div 
                class="h-full rounded-full transition-all duration-1000"
                :class="getProbabilityColor(diff.probability)"
                :style="`width: ${getProbabilityWidth(diff.probability)}`"
              ></div>
            </div>
            <!-- Reasoning Display -->
            <p v-if="diff.reasoning" class="text-[10px] text-slate-500 leading-tight italic border-l-2 border-slate-200 pl-2 mt-1">
              {{ diff.reasoning }}
            </p>
          </div>
        </div>
      </div>

      <!-- Recommended Tests -->
      <div v-if="insights?.recommended_tests?.length" class="space-y-3 animate-fade-in delay-100">
        <label class="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
          <BeakerIcon class="h-3 w-3" /> Pruebas Sugeridas
        </label>
        
        <div class="bg-indigo-50/50 rounded-xl p-3 border border-indigo-100 space-y-3">
          <div v-for="(test, idx) in insights.recommended_tests" :key="idx" class="flex items-start gap-2">
            <div class="mt-0.5 min-w-[14px]">
              <div class="w-3.5 h-3.5 rounded border border-indigo-300 bg-white flex items-center justify-center">
                <CheckIcon class="h-2.5 w-2.5 text-indigo-600 opacity-0 hover:opacity-100 cursor-pointer transition-opacity" />
              </div>
            </div>
            <div>
              <span class="text-xs text-slate-700 font-bold leading-tight block">{{ typeof test === 'string' ? test : test.name }}</span>
              <span v-if="test.purpose" class="text-[10px] text-slate-500 leading-tight block mt-0.5">{{ test.purpose }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Treatment Focus -->
      <div v-if="insights?.treatment_focus?.length" class="space-y-3 animate-fade-in delay-200">
        <label class="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
          <HeartIcon class="h-3 w-3" /> Enfoque Terapéutico
        </label>
        
        <div class="flex flex-wrap gap-2">
          <span 
            v-for="(focus, idx) in insights.treatment_focus" 
            :key="idx"
            class="inline-flex items-center px-2.5 py-1 rounded-lg text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-100"
          >
            {{ focus }}
          </span>
        </div>
      </div>

      <!-- Smart Dosage Calculator -->
      <div v-if="insights?.calculated_dosages?.length" class="space-y-3 animate-fade-in delay-200">
        <label class="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center gap-1">
          <CalculatorIcon class="h-3 w-3" /> Dosis Inteligentes
        </label>
        
        <div class="space-y-2">
          <div v-for="(dose, idx) in insights.calculated_dosages" :key="idx" class="bg-blue-50 rounded-xl p-3 border border-blue-100 relative overflow-hidden">
            <div class="absolute top-0 right-0 p-1 opacity-10">
              <BeakerIcon class="w-8 h-8 text-blue-600" />
            </div>
            <div class="relative z-10">
              <div class="font-bold text-xs text-blue-900">{{ dose.drug }}</div>
              <div class="flex items-baseline gap-1 mt-1">
                <span class="text-lg font-bold text-blue-700">{{ dose.dose }}</span>
                <span class="text-[10px] text-blue-600">{{ dose.frequency }}</span>
              </div>
              <div class="text-[9px] text-blue-400 mt-1 italic">{{ dose.notes }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Safety Alerts -->
      <div v-if="insights?.safety_alerts?.length" class="space-y-3 animate-fade-in delay-200">
        <label class="text-xs font-bold text-rose-500 uppercase tracking-wider flex items-center gap-1">
          <ExclamationTriangleIcon class="h-3 w-3" /> Alertas de Seguridad
        </label>
        
        <div class="space-y-2">
          <div v-for="(alert, idx) in insights.safety_alerts" :key="idx" 
            class="rounded-xl p-3 border flex gap-2 items-start"
            :class="{
              'bg-rose-50 border-rose-100 text-rose-700': alert.level.includes('High') || alert.level.includes('Alta'),
              'bg-amber-50 border-amber-100 text-amber-700': alert.level.includes('Medium') || alert.level.includes('Media'),
              'bg-blue-50 border-blue-100 text-blue-700': alert.level.includes('Low') || alert.level.includes('Baja')
            }"
          >
            <ExclamationTriangleIcon class="h-4 w-4 shrink-0 mt-0.5" />
            <div class="text-xs font-medium leading-tight">{{ alert.message }}</div>
          </div>
        </div>
      </div>

      <!-- Smart Follow-up -->
      <div v-if="insights?.follow_up" class="space-y-3 animate-fade-in delay-300">
        <label class="text-xs font-bold text-indigo-500 uppercase tracking-wider flex items-center gap-1">
          <CalendarDaysIcon class="h-3 w-3" /> Seguimiento Inteligente
        </label>
        
        <div class="bg-indigo-50 border border-indigo-100 rounded-xl p-3">
          <div class="flex justify-between items-start mb-2">
            <div>
              <div class="text-sm font-bold text-indigo-900">{{ insights.follow_up.duration }}</div>
              <div class="text-[10px] text-indigo-600 leading-tight mt-0.5">{{ insights.follow_up.reason }}</div>
            </div>
            <button 
              @click="$emit('schedule', insights.follow_up)"
              class="bg-indigo-600 text-white text-[10px] font-bold px-2 py-1 rounded-lg shadow-sm hover:bg-indigo-700 transition-colors"
            >
              Agendar
            </button>
          </div>
        </div>
      </div>

      <!-- References -->
      <div v-if="insights?.references?.length" class="space-y-3 animate-fade-in delay-300 pt-2 border-t border-slate-100">
        <label class="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
          Referencias & Guías
        </label>
        <ul class="list-disc list-inside space-y-1">
          <li v-for="(ref, idx) in insights.references" :key="idx" class="text-[9px] text-slate-500 leading-tight">
            {{ ref }}
          </li>
        </ul>
      </div>

      <div v-if="!insights" class="flex flex-col items-center justify-center py-10 opacity-40 text-center">
        <SparklesIcon class="h-10 w-10 text-slate-300 mb-2" />
        <p class="text-xs text-slate-400">Analizando conversación...</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { 
  LightBulbIcon, 
  ChartPieIcon, 
  BeakerIcon, 
  HeartIcon, 
  CheckIcon,
  SparklesIcon,
  CalculatorIcon,
  ExclamationTriangleIcon,
  CalendarDaysIcon
} from '@heroicons/vue/24/outline';

defineProps({
  insights: {
    type: Object,
    default: null
  }
});

const getProbabilityWidth = (prob) => {
  const p = prob.toLowerCase();
  if (p.includes('alta') || p.includes('high')) return '85%';
  if (p.includes('media') || p.includes('medium')) return '50%';
  if (p.includes('baja') || p.includes('low')) return '25%';
  return '10%';
};

const getProbabilityColor = (prob) => {
  const p = prob.toLowerCase();
  if (p.includes('alta') || p.includes('high')) return 'bg-rose-500';
  if (p.includes('media') || p.includes('medium')) return 'bg-amber-500';
  return 'bg-emerald-500';
};
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

.animate-fade-in {
  animation: fadeIn 0.5s ease-out forwards;
}

.delay-100 { animation-delay: 150ms; }
.delay-200 { animation-delay: 300ms; }

@keyframes fadeIn {
  to { opacity: 1; }
}
</style>
