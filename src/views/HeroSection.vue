<template>
  <section class="relative w-screen h-screen overflow-hidden">
    
    <header class="absolute top-0 left-0 w-full z-20 flex justify-end py-5 px-8">
      <nav class="flex items-center justify-center gap-4 md:gap-5 mr-16">
        
        <a href="#" class="bg-[#02939E80] backdrop-blur-lg text-white text-base md:text-lg font-medium py-4 px-10 md:px-12 rounded-lg shadow-xl hover:scale-105 transition-all duration-300 ease-in-out w-60 text-center">Servicios</a>
        <a href="#" class="bg-[#02939E80] backdrop-blur-lg text-white text-base md:text-lg font-medium py-4 px-10 md:px-12 rounded-lg shadow-xl hover:scale-105 transition-all duration-300 ease-in-out w-60 text-center">Pet Shop</a>
        <a href="#" class="bg-[#02939E80] backdrop-blur-lg text-white text-base md:text-lg font-medium py-4 px-10 md:px-12 rounded-lg shadow-xl hover:scale-105 transition-all duration-300 ease-in-out w-60 text-center">Adopción online</a>
        
        <a href="#" 
           aria-label="Mi Cuenta" 
           class="flex items-center justify-center bg-[#a4ad7480] backdrop-blur-lg rounded-lg shadow-xl hover:scale-105 transition-all duration-300 ease-in-out h-14 w-14 md:h-[60px] md:w-[60px]">
           
           <svg 
             xmlns="http://www.w3.org/2000/svg" 
             viewBox="0 0 24 24" 
             fill="white" 
             class="w-8 h-8">
            <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z" clip-rule="evenodd" />
          </svg>
        </a>
      </nav>
    </header>

    
    <div class="absolute inset-0 w-full h-full">
      <img class="w-full h-full object-cover" :src="principalImage" alt="Veterinaria - Ilustración principal" />
      <div class="absolute inset-0 bg-black/50"></div> 
    </div>

    <svg
      class="absolute bottom-0 left-0 w-full z-10"
      style="height: 120px;" viewBox="0 0 1440 120"
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      <defs>
        <filter id="waveBlur" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="6" />
        </filter>
      </defs>

      <path
        d="M1440,80 C1200,40 960,40 720,80 C480,120 240,120 0,80 L0,120 L1440,120 Z"
        fill="rgba(0,0,0,0.15)" filter="url(#waveBlur)"
        transform="translate(0, 10)" />

      <path
        d="M1440,80 C1200,40 960,40 720,80 C480,120 240,120 0,80 L0,120 L1440,120 Z"
        fill="#FFFFFF" />
    </svg>

    <img :src="patitasImage" alt="Patas de perro" class="absolute bottom-8 left-0 w-56 z-20 opacity-70" />

    <div class="absolute z-40 text-white p-8 max-w-3xl text-left top-48 left-0 ml-12 md:ml-20">
      <h1 class="text-6xl font-serif leading-tight mb-4 tracking-wide">
        COMPROMETIDOS CON LA salud Y EL bienestar animal.
      </h1>
      <p class="text-2xl font-serif italic">Más que veterinaria, un hogar para tu mascota.</p>
    </div>

  </section>
</template>

<script setup>
import principalImage from '@/assets/images/principal.svg';
import patitasImage from '@/assets/images/patitas.svg';
</script>