<template>
  <section class="relative w-screen h-screen overflow-hidden">
    
    <header class="absolute top-0 left-0 w-full z-20 flex justify-end py-5 px-8">
      <nav class="flex items-center justify-center gap-4 md:gap-5 mr-16">
        <a href="#" class="bg-[#02939E80] backdrop-blur-lg text-white text-base md:text-lg font-medium py-4 px-10 md:px-12 rounded-lg shadow-xl hover:scale-105 transition-all duration-300 ease-in-out w-60 text-center">Servicios</a>
        <a href="#" class="bg-[#02939E80] backdrop-blur-lg text-white text-base md:text-lg font-medium py-4 px-10 md:px-12 rounded-lg shadow-xl hover:scale-105 transition-all duration-300 ease-in-out w-60 text-center">Pet Shop</a>
        <a href="#" class="bg-[#02939E80] backdrop-blur-lg text-white text-base md:text-lg font-medium py-4 px-10 md:px-12 rounded-lg shadow-xl hover:scale-105 transition-all duration-300 ease-in-out w-60 text-center">Adopción online</a>
      </nav>
    </header>

    <aside class="fixed top-1/2 right-0 transform -translate-y-1/2 z-30 flex flex-col gap-2 mr-2">
      <a href="https://www.facebook.com/" target="_blank" rel="noopener noreferrer" aria-label="Síguenos en Facebook"
         class="flex items-center justify-center bg-[#02939E80] backdrop-blur-lg text-white rounded-lg shadow-xl hover:scale-105 transition-all py-4 px-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 16 16">
          <path d="M16 8.049c0-4.446-3.582-8.05-8-8.05C3.58 0-.002 3.603-.002 8.05c0 4.017 2.926 7.347 6.75 7.951v-5.625h-2.03V8.05H6.75V6.275c0-2.017 1.195-3.131 3.022-3.131.876 0 1.791.157 1.791.157v1.98h-1.009c-.993 0-1.303.621-1.303 1.258v1.51h2.218l-.354 2.326H9.25V16c3.824-.604 6.75-3.934 6.75-7.951z"/>
        </svg>
      </a>
      <a href="https://wa.me/TUNUMERO" target="_blank" rel="noopener noreferrer" aria-label="Contáctanos por WhatsApp"
         class="flex items-center justify-center bg-[#02939E80] backdrop-blur-lg text-white rounded-lg shadow-xl hover:scale-105 transition-all py-4 px-4">
        <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" fill="currentColor" viewBox="0 0 16 16">
          <path d="M13.601 2.326A7.854 7.854 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.933 7.933 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.898 7.898 0 0 0 13.6 2.326zM7.994 14.521a6.573 6.573 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.557 6.557 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592zm3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.729.729 0 0 0-.529.247c-.182.198-.691.677-.691 1.654 0 .977.71 1.916.81 2.049.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232z"/>
        </svg>
      </a>
    </aside>
    
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
        fill="#FFFFFF" stroke="#ADD8E6" stroke-width="4" />
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

<style scoped>
/* No se necesitan estilos adicionales para este SVG, ya que todo está inline. */
</style>