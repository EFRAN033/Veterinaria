<template>
  <div class="owner-contact-root border-t-2 border-gray-100 pt-10 mt-10">
    <div class="border-l-4 border-[#1BB0B9] pl-6 mb-6">
      <h2 class="app-type-panel-heading">Datos del contacto</h2>
      <p class="text-gray-500 text-sm mt-1">
        Persona a la que podremos escribir o llamar sobre esta solicitud (no tiene que ser el titular de la mascota).
      </p>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8 p-6 bg-gray-50 border-2 border-gray-100 rounded-none">
      <div class="group relative md:col-span-2">
        <input
          type="text"
          :value="modelValue.ownerName"
          maxlength="120"
          placeholder=" "
          class="floating-input peer"
          autocomplete="name"
          @input="patch({ ownerName: $event.target.value })"
        />
        <label class="floating-label">Nombre completo</label>
      </div>
      <div class="group relative">
        <input
          type="tel"
          inputmode="numeric"
          :value="modelValue.ownerPhone"
          maxlength="9"
          placeholder=" "
          class="floating-input peer"
          autocomplete="tel-national"
          @input="onPhoneInput($event)"
        />
        <label class="floating-label">Número de celular</label>
      </div>
      <div class="group relative">
        <input
          type="email"
          :value="modelValue.ownerEmail"
          maxlength="120"
          placeholder=" "
          class="floating-input peer"
          autocomplete="email"
          @input="patch({ ownerEmail: $event.target.value })"
        />
        <label class="floating-label">Correo electrónico</label>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['update:modelValue']);

function patch(partial) {
  emit('update:modelValue', { ...props.modelValue, ...partial });
}

function onPhoneInput(e) {
  const digits = e.target.value.replace(/\D/g, '').slice(0, 9);
  e.target.value = digits;
  patch({ ownerPhone: digits });
}
</script>

<style scoped>
.floating-input {
  @apply block px-4 pb-2.5 pt-5 w-full text-gray-900 bg-white border-2 border-gray-100 rounded-none appearance-none focus:outline-none focus:ring-0 focus:border-[#1BB0B9] transition-all;
}

.floating-label {
  @apply absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] left-4 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 peer-focus:text-[#1BB0B9] pointer-events-none font-bold;
}
</style>
