<template>
  <section class="relative w-screen h-screen overflow-hidden">
    
    <header class="absolute top-0 left-0 w-full z-10 flex justify-end py-5 px-8">
      <nav class="flex items-center justify-center gap-4 md:gap-5 mr-16">
        <a 
          href="#" 
          class="bg-[#02939E80] backdrop-blur-lg text-white text-base md:text-lg font-medium py-4 px-10 md:px-12 rounded-lg shadow-xl transform hover:scale-105 transition-all duration-300 ease-in-out w-60 text-center">
          Servicios
        </a>
        <a 
          href="#" 
          class="bg-[#02939E80] backdrop-blur-lg text-white text-base md:text-lg font-medium py-4 px-10 md:px-12 rounded-lg shadow-xl transform hover:scale-105 transition-all duration-300 ease-in-out w-60 text-center">
          Pet Shop
        </a>
        <a 
          href="#" 
          class="bg-[#02939E80] backdrop-blur-lg text-white text-base md:text-lg font-medium py-4 px-10 md:px-12 rounded-lg shadow-xl transform hover:scale-105 transition-all duration-300 ease-in-out w-60 text-center">
          Adopción online
        </a>
      </nav>
    </header>

    <div class="absolute inset-0 w-full h-full">
      <img 
        class="w-full h-full object-cover" 
        :src="principalImage" 
        alt="Veterinaria - Ilustración principal"
      />
      <div class="absolute inset-0 bg-black/50"></div> 
    </div>

    <div class="absolute z-10 text-white p-8 max-w-3xl text-left top-48 left-0 ml-12 md:ml-20">
      <h1 class="text-6xl font-serif leading-tight mb-4 tracking-wide">
        COMPROMETIDOS CON LA salud Y EL bienestar animal.
      </h1>
      <p class="text-2xl font-serif italic">
        Más que veterinaria, un hogar para tu mascota.
      </p>
    </div>

  </section>
</template>

<script setup>
import principalImage from '@/assets/images/principal.svg';
</script>

<style scoped>
/* Estilos adicionales si fueran necesarios */
</style>