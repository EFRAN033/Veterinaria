<template>
  <div :class="containerClasses" class="loading-spinner" role="status" :aria-label="ariaLabel">
    <svg
      :class="spinnerClasses"
      class="animate-spin"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
    <span v-if="text" :class="textClasses" class="ml-3">{{ text }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value),
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'white', 'gray'].includes(value),
  },
  text: {
    type: String,
    default: '',
  },
  centered: {
    type: Boolean,
    default: false,
  },
  ariaLabel: {
    type: String,
    default: 'Cargando...',
  },
});

const sizeClasses = {
  xs: 'w-3 h-3',
  sm: 'w-4 h-4',
  md: 'w-6 h-6',
  lg: 'w-8 h-8',
  xl: 'w-12 h-12',
};

const colorClasses = {
  primary: 'text-[#1BB0B9]',
  secondary: 'text-[#BEDC74]',
  white: 'text-white',
  gray: 'text-gray-400',
};

const textSizeClasses = {
  xs: 'text-xs',
  sm: 'text-sm',
  md: 'text-base',
  lg: 'text-lg',
  xl: 'text-xl',
};

const spinnerClasses = computed(() => {
  return [sizeClasses[props.size], colorClasses[props.color]];
});

const textClasses = computed(() => {
  return [textSizeClasses[props.size], colorClasses[props.color], 'font-medium'];
});

const containerClasses = computed(() => {
  return {
    'flex items-center': true,
    'justify-center': props.centered,
  };
});
</script>

<style scoped>
.loading-spinner {
  @apply inline-flex;
}
</style>
