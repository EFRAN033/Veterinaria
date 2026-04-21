<template>
  <section class="relative w-full min-h-screen min-w-0 font-sans bg-black overflow-x-hidden overflow-y-hidden flex flex-col justify-between">
    
    <Header />

    <div class="absolute inset-0 bg-black overflow-hidden">
      <img
        class="absolute inset-0 h-full w-full object-cover object-center"
        :src="principalImage"
        alt="Veterinaria - Ilustración principal"
      />
      <div class="absolute inset-0 bg-black/75" aria-hidden="true"></div>
    </div>

    <div class="relative z-30 container mx-auto px-8 md:px-16 flex flex-col justify-center flex-grow h-full pb-20">
      <div class="max-w-3xl mt-10 md:mt-0">
        <h1 class="app-type-hero mb-5">
          Comprometidos con <br/>
          <span class="text-[#a4ad74]">su salud y bienestar.</span>
        </h1>
        
        <p class="app-type-lead-on-dark mb-8">
          Más que una veterinaria, somos un segundo hogar para tu mascota.
        </p>

        <div class="flex flex-col sm:flex-row gap-3">
          <router-link to="/servicios" class="app-btn-cta-primary text-center sm:inline-flex">
            Agendar Cita
          </router-link>
          <button type="button" class="app-btn-cta-outline-light">
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
import Header from './Header.vue';
</script>