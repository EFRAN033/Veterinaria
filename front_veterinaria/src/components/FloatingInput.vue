<template>
  <div class="group relative">
    <input 
      :id="id"
      :type="type"
      :value="modelValue"
      @input="handleInput"
      @blur="handleBlur"
      placeholder=" "
      :required="required"
      :disabled="disabled"
      :class="inputClasses"
      class="floating-input peer"
      v-bind="$attrs"
    />
    <label :for="id" class="floating-label">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    
    <!-- Icon slot (right side) -->
    <div v-if="$slots.icon" class="absolute right-4 top-1/2 -translate-y-1/2">
      <slot name="icon" />
    </div>
    
    <!-- Error message -->
    <transition name="slide-down">
      <div v-if="error" class="text-red-500 text-xs mt-1.5 ml-1 flex items-center gap-1">
        <svg class="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        <span>{{ error }}</span>
      </div>
    </transition>
    
    <!-- Helper text -->
    <p v-if="helperText && !error" class="text-xs text-gray-400 mt-1.5 ml-1">
      {{ helperText }}
    </p>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  label: {
    type: String,
    required: true,
  },
  error: {
    type: String,
    default: '',
  },
  helperText: {
    type: String,
    default: '',
  },
  required: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substr(2, 9)}`,
  },
});

const emit = defineEmits(['update:modelValue', 'blur']);

const isTouched = ref(false);

const handleInput = (event) => {
  emit('update:modelValue', event.target.value);
};

const handleBlur = (event) => {
  isTouched.value = true;
  emit('blur', event);
};

const inputClasses = computed(() => ({
  'border-red-300 focus:border-red-500 focus:ring-red-500/10': props.error,
  'border-gray-100 focus:border-[#1BB0B9] focus:ring-[#1BB0B9]/10': !props.error,
  'opacity-50 cursor-not-allowed': props.disabled,
}));
</script>

<style scoped>
.floating-input {
  @apply block px-4 pb-2.5 pt-5 w-full text-gray-900 bg-gray-50 border-2 rounded-xl appearance-none 
  focus:outline-none focus:ring-4 transition-all duration-300;
}

.floating-input:focus {
  @apply bg-white;
}

.floating-label {
  @apply absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] left-4 
  peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 
  peer-focus:scale-75 peer-focus:-translate-y-4 peer-focus:text-[#1BB0B9] 
  pointer-events-none font-bold;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.2s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-4px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
