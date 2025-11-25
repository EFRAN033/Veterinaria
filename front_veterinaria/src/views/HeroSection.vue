<template>
  <section class="relative w-full min-h-screen font-sans bg-gray-900 overflow-hidden flex flex-col justify-between">
    
    <Header />

    <div class="absolute inset-0 w-full h-full">
      <img class="w-full h-full object-cover object-center" :src="principalImage" alt="Veterinaria - Ilustración principal" />
      <div class="absolute inset-0 bg-gradient-to-r from-black/80 via-black/40 to-transparent"></div> 
    </div>

    <div class="relative z-30 container mx-auto px-8 md:px-16 flex flex-col justify-center flex-grow h-full pb-20">
      <div class="max-w-3xl mt-10 md:mt-0">
        <h1 class="text-5xl md:text-7xl text-white font-serif font-bold leading-tight mb-6 tracking-wide">
          Comprometidos con <br/>
          <span class="text-[#a4ad74]">su salud y bienestar.</span>
        </h1>
        
        <p class="text-xl md:text-2xl text-gray-200 font-light mb-10 max-w-lg italic">
          Más que una veterinaria, somos un segundo hogar para tu mascota.
        </p>

        <div class="flex flex-col sm:flex-row gap-4">
          <router-link to="/servicios" class="bg-[#02939E] text-white px-8 py-4 rounded-lg text-lg font-bold shadow-lg hover:bg-[#027a83] transition-transform hover:-translate-y-1 inline-block text-center">
            Agendar Cita
          </router-link>
          <button class="border-2 border-white text-white px-8 py-4 rounded-lg text-lg font-medium hover:bg-white hover:text-black transition-colors">
            Conócenos
          </button>
        </div>
      </div>
    </div>

    <div class="relative w-full z-20 leading-[0]">
        <img 
          :src="patitasImage" 
          alt="Patas de perro" 
          class="absolute bottom-4 left-8 w-32 md:w-40 z-30 opacity-50 rotate-12 hidden md:block" 
        />
        <svg class="relative block w-[calc(100%+1.3px)] h-[60px] md:h-[100px]" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
            <path d="M0,80 C300,110 800,40 1200,90 L1200,120 L0,120 Z" fill="#FFFFFF"></path>
        </svg>
    </div>

  </section>
</template>

<script setup>
import principalImage from '@/assets/images/principal.svg';
import patitasImage from '@/assets/images/patitas.svg';
// Importamos el nuevo componente
import Header from './Header.vue';
</script>