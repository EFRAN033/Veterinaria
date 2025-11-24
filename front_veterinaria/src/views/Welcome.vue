<template>
  <section class="bg-white w-full py-20 md:py-32 font-sans overflow-hidden">
    
    <div class="container mx-auto px-8 md:px-16">
      <div class="flex flex-col lg:flex-row items-center gap-16">
        
        <div class="flex-1 text-left space-y-8">
          
          <div>
            <span class="text-[#a4ad74] font-bold tracking-[0.2em] uppercase text-sm md:text-base block mb-2">
              Sobre Nosotros
            </span>
            <h2 class="text-4xl md:text-5xl font-serif font-bold text-gray-900 leading-tight">
              Bienvenido a <br/>
              <span class="text-[#02939E]">Clínica Velit</span>
            </h2>
            <div class="w-20 h-1 bg-[#a4ad74] mt-6"></div>
          </div>

          <p class="text-lg md:text-xl text-gray-600 leading-relaxed font-light max-w-xl">
            Creemos que cada mascota es un miembro más de la familia. En 
            <strong class="text-gray-800 font-medium">Velit</strong>, combinamos la pasión por los animales con la excelencia médica.
            Nuestro compromiso es brindar una atención personalizada, donde el amor y la ciencia se unen para el bienestar de tu mejor amigo.
          </p>

          <ul class="space-y-4 mt-4">
            <li class="flex items-center gap-3 text-gray-700">
              <div class="w-2 h-2 rounded-full bg-[#02939E]"></div>
              <span>Atención veterinaria integral 24/7</span>
            </li>
            <li class="flex items-center gap-3 text-gray-700">
              <div class="w-2 h-2 rounded-full bg-[#02939E]"></div>
              <span>Tecnología de diagnóstico avanzada</span>
            </li>
            <li class="flex items-center gap-3 text-gray-700">
              <div class="w-2 h-2 rounded-full bg-[#02939E]"></div>
              <span>Equipo apasionado y certificado</span>
            </li>
          </ul>

          <div class="pt-4">
            <a href="#" class="inline-flex items-center justify-center px-8 py-4 text-lg font-bold text-white transition-all duration-300 bg-[#02939E] rounded-lg hover:bg-[#027a83] hover:-translate-y-1 shadow-lg shadow-[#02939E]/30">
              Conoce Nuestros Servicios
            </a>
          </div>
        </div>

        <div class="flex-1 relative flex justify-center lg:justify-end">
          
          <div class="relative z-10 rounded-2xl overflow-hidden shadow-2xl">
            <img 
              :src="humanDogImage" 
              alt="Veterinario cuidando a un perro" 
              class="w-full max-w-md lg:max-w-lg object-cover" 
            />
          </div>

        </div>

      </div>
    </div>
  </section>
</template>

<script setup>
import humanDogImage from '@/assets/images/humandog.png'; 
</script>