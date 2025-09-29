<template>
    <section class="relative w-screen h-screen flex items-center justify-center overflow-hidden">
      <div class="absolute inset-0 w-full h-full">
        <img 
          class="w-full h-full object-cover" 
          :src="principalImage" 
          alt="Veterinaria - Ilustración principal"
        />
      </div>
    </section>
  </template>
  
  <script setup>
  // Importación explícita del recurso desde src/assets/images
  import principalImage from '@/assets/images/principal.svg';
  </script>
  
  <style scoped>
  /*
    No se necesitan estilos adicionales aquí, ya que las clases de Tailwind
    'w-screen', 'h-screen', 'absolute', 'inset-0', 'w-full', 'h-full',
    y 'object-cover' se encargan de todo.
  */
  </style>