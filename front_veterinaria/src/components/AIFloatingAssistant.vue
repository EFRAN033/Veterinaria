<template>
  <div v-if="questions.length > 0" class="fixed bottom-24 right-6 z-50 flex flex-col items-end gap-2 animate-fade-in-up">
    
    <div class="bg-indigo-600 text-white text-xs font-bold px-3 py-1.5 rounded-full shadow-lg flex items-center gap-2 mb-1 animate-bounce-slow">
      <SparklesIcon class="h-4 w-4" />
      <span>Sugerencias IA</span>
    </div>

    <button 
      v-for="(question, index) in questions" 
      :key="index"
      @click="$emit('select', question)"
      class="bg-white hover:bg-indigo-50 text-slate-700 hover:text-indigo-700 text-xs font-medium px-4 py-3 rounded-xl shadow-lg border border-slate-200 hover:border-indigo-200 transition-all duration-300 transform hover:-translate-x-1 hover:scale-105 text-right max-w-xs"
    >
      {{ question }}
    </button>
  </div>
</template>

<script setup>
import { SparklesIcon } from '@heroicons/vue/24/solid';

defineProps({
  questions: {
    type: Array,
    default: () => []
  }
});

defineEmits(['select']);
</script>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
}

.animate-bounce-slow {
  animation: bounce 3s infinite;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
</style>
