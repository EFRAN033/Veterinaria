<template>
  <section class="bg-gray-50 min-h-screen flex flex-col pt-20 pb-20">
    
    <div class="w-full text-center">
      <h1 class="text-6xl font-serif text-gray-800 tracking-widest mb-4">
        BIENVENIDO
      </h1>
      <div class="w-32 h-1 bg-teal-600 mx-auto"></div>
    </div>

    <div class="w-full flex justify-center px-8 md:px-24 mt-16">
      
      <div class="flex flex-col md:flex-row items-center bg-white p-8 md:p-12 rounded-lg shadow-xl max-w-6xl">
        
        <div class="max-w-2xl md:mr-12">
          
          <h2 class="text-3xl font-serif font-bold text-teal-700 mb-4">
            Amor y cuidado profesional
          </h2>

          <p class="text-2xl text-gray-700 leading-relaxed font-serif text-left mb-8">
            En la clinica veterinaria Velit, creemos que cada mascota merece una vida llena de salud, amor y bienestar. Somos un equipo apasionado por el cuidado animal, comprometido con brindar atención veterinaria de calidad, personalizada y con el cariño que tu mejor amigo necesita.
          </p>

          <a href="#" class="inline-block bg-teal-600 text-white font-bold py-3 px-8 rounded-lg text-lg hover:bg-teal-700 transition-colors duration-300">
            Nuestros Servicios
          </a>
        </div>

        <div class="mt-8 md:mt-0">
          <img :src="humanDogImage" alt="Human with dog" class="max-w-xs lg:max-w-sm rounded-lg" />
        </div>

      </div>
    </div>

  </section>
</template>

<script setup>
import humanDogImage from '@/assets/images/humandog.png'; 
</script>

<style scoped>
/* Estilos adicionales si los necesitas. */
</style>