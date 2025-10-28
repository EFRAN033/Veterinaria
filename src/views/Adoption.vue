<template>
    <section id="adopcion" class="w-full py-20 px-4 md:px-12 bg-gray-50">
      
      <div class="max-w-7xl mx-auto">
  
        <div class="bg-gradient-to-b from-[#1A97A1] to-[#1BD1DF] rounded-2xl shadow-xl p-8 md:p-12">
  
          <div class="text-center mb-12">
            <h2 class="text-4xl md:text-5xl font-sans font-light text-white tracking-widest uppercase">
              Adopción Online
            </h2>
          </div>
  
          <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            
            <a href="#" class="relative rounded-lg shadow-lg overflow-hidden transition-all duration-300 group">
              <img :src="gatoImage" alt="Gatos en adopción" class="w-full h-64 object-cover">
              <div class="absolute inset-x-0 bottom-0 z-30 px-4">
                <img :src="senalgatoImage" alt="Señal de gato" class="w-full h-12 object-cover rounded-t-md">
              </div>
              <div class="absolute inset-x-0 bottom-0 z-40 h-12 flex items-center justify-center">
                <span class="text-gray-900 text-2xl font-serif font-semibold">
                  Gatos
                </span>
              </div>
            </a>
  
            <a href="#" class="relative rounded-lg shadow-lg overflow-hidden transition-all duration-300 group">
              <img :src="perroImage" alt="Perros en adopción" class="w-full h-64 object-cover">
              <div class="absolute inset-x-0 bottom-0 z-30 px-4">
                <img :src="senalperroImage" alt="Señal de perro" class="w-full h-12 object-cover rounded-t-md">
              </div>
              <div class="absolute inset-x-0 bottom-0 z-40 h-12 flex items-center justify-center">
                <span class="text-gray-900 text-2xl font-serif font-semibold">
                  Perros
                </span>
              </div>
            </a>
  
            <a href="#" class="relative rounded-lg shadow-lg overflow-hidden transition-all duration-300 group">
              <img :src="hamsterImage" alt="Hámsters en adopción" class="w-full h-64 object-cover">
              <div class="absolute inset-x-0 bottom-0 z-30 px-4">
                <img :src="senalhamsterImage" alt="Señal de hámster" class="w-full h-12 object-cover rounded-t-md">
              </div>
              <div class="absolute inset-x-0 bottom-0 z-40 h-12 flex items-center justify-center">
                <span class="text-gray-900 text-2xl font-serif font-semibold">
                  Hamsters
                </span>
              </div>
            </a>

            <a href="#" class="relative rounded-lg shadow-lg overflow-hidden transition-all duration-300 group">
              <img :src="pecesImage" alt="Peces en adopción" class="w-full h-64 object-cover">
              <div class="absolute inset-x-0 bottom-0 z-30 px-4">
                <img :src="senalgatoImage" alt="Señal de peces" class="w-full h-12 object-cover rounded-t-md">
              </div>
              <div class="absolute inset-x-0 bottom-0 z-40 h-12 flex items-center justify-center">
                <span class="text-gray-900 text-2xl font-serif font-semibold">
                  Peces
                </span>
              </div>
            </a>
  
          </div>
  
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import gatoImage from '@/assets/images/gato.png';
  import perroImage from '@/assets/images/perro.png';
  import hamsterImage from '@/assets/images/hamster.png';
  import pecesImage from '@/assets/images/peces.png';
  
  // Importaciones de las imágenes de señal
  import senalgatoImage from '@/assets/images/senalgato.png'; 
  import senalperroImage from '@/assets/images/senalperro.png';
  import senalhamsterImage from '@/assets/images/senalhamster.png';
  // CAMBIO: Se eliminó la importación de senalpez.png
 </script>
  
  <style scoped>
  /* Puedes añadir estilos específicos aquí si lo necesitas */
  </style>