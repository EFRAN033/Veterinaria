<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    class="base-button group"
    @click="handleClick"
  >
    <!-- Loading spinner -->
    <svg
      v-if="loading"
      class="animate-spin w-5 h-5"
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

    <!-- Icon slot (left) -->
    <slot v-if="!loading && $slots.icon" name="icon" />

    <!-- Button text -->
    <span v-if="!loading">
      <slot />
    </span>
    <span v-else>
      {{ loadingText }}
    </span>

    <!-- Arrow icon for primary buttons -->
    <svg
      v-if="!loading && variant === 'primary' && !$slots.iconRight"
      class="w-5 h-5 transform group-hover:translate-x-1 transition-transform"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M17 8l4 4m0 0l-4 4m4-4H3"
      />
    </svg>

    <!-- Icon slot (right) -->
    <slot v-if="!loading && $slots.iconRight" name="iconRight" />
  </button>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value),
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'outline', 'ghost', 'danger'].includes(value),
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  loading: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  loadingText: {
    type: String,
    default: 'Procesando...',
  },
  fullWidth: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(['click']);

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event);
  }
};

const buttonClasses = computed(() => {
  const classes = [];

  // Size classes
  const sizeClasses = {
    sm: 'py-2 px-4 text-sm',
    md: 'py-3 px-6 text-base',
    lg: 'py-4 px-8 text-lg',
  };
  classes.push(sizeClasses[props.size]);

  // Variant classes
  const variantClasses = {
    primary: 'bg-gradient-to-r from-[#1BB0B9] to-[#16a0a8] text-white hover:shadow-lg hover:shadow-[#1BB0B9]/40',
    secondary: 'bg-gradient-to-r from-[#BEDC74] to-[#a8c965] text-white hover:shadow-lg hover:shadow-[#BEDC74]/30',
    outline: 'border-2 border-[#1BB0B9] text-[#1BB0B9] hover:bg-[#1BB0B9]/5',
    ghost: 'text-[#1BB0B9] hover:bg-[#1BB0B9]/5',
    danger: 'bg-red-500 text-white hover:bg-red-600 hover:shadow-lg hover:shadow-red-500/40',
  };
  classes.push(variantClasses[props.variant]);

  // Width class
  if (props.fullWidth) {
    classes.push('w-full');
  }

  // Disabled/Loading state
  if (props.disabled || props.loading) {
    classes.push('opacity-50 cursor-not-allowed');
  }

  return classes.join(' ');
});
</script>

<style scoped>
.base-button {
  @apply font-bold rounded-xl transition-all duration-300 
  flex items-center justify-center gap-2 
  active:scale-95
  focus:outline-none focus:ring-4 focus:ring-[#1BB0B9]/20;
}

.base-button:disabled {
  @apply transform-none shadow-none;
}
</style>
