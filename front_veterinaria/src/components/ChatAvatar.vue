<template>
  <div class="shrink-0 h-8 w-8 flex items-center justify-center transition-colors duration-500">
    <UserIcon 
      v-if="role === 'user'" 
      class="h-6 w-6 transition-colors duration-500"
      :class="isLatest ? 'text-indigo-700' : 'text-slate-300'" 
    />

    <SparklesIcon 
      v-else 
      class="h-6 w-6 transition-all duration-500"
      :class="[
        isLatest ? 'text-cyan-400 drop-shadow-[0_0_8px_rgba(34,211,238,0.6)]' : 'text-slate-300',
        { 'animate-thinking': isAnimated }
      ]"
    />
  </div>
</template>

<script setup>
import { UserIcon, SparklesIcon } from '@heroicons/vue/24/solid';

defineProps({
  role: {
    type: String,
    required: true,
    validator: (value) => ['user', 'assistant'].includes(value)
  },
  isAnimated: {
    type: Boolean,
    default: false
  },
  isLatest: {
    type: Boolean,
    default: false
  }
});
</script>

<style scoped>
@keyframes thinking {
  0% {
    transform: rotate(0deg) scale(1);
    filter: drop-shadow(0 0 5px rgba(34,211,238,0.5));
  }
  50% {
    /* A la mitad del pensamiento: Gira, crece un poco y brilla más */
    transform: rotate(180deg) scale(1.15);
    filter: drop-shadow(0 0 12px rgba(34,211,238,0.9));
  }
  100% {
    transform: rotate(360deg) scale(1);
    filter: drop-shadow(0 0 5px rgba(34,211,238,0.5));
  }
}

.animate-thinking {
  /* 2.5 segundos es el ritmo ideal para parecer "inteligente" y no solo "cargando" */
  animation: thinking 2.5s infinite ease-in-out;
}
</style>