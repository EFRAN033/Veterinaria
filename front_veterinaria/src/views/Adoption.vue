<template>
  <section id="adopcion" class="w-full py-20 px-4 md:px-16 bg-white font-sans overflow-hidden">
    
    <div class="max-w-7xl mx-auto">

      <div class="text-center mb-16">
        <span class="text-[#a4ad74] font-bold tracking-[0.2em] uppercase text-sm block mb-3">
          Tu futuro mejor amigo
        </span>
        <h2 class="text-4xl md:text-5xl font-serif font-bold text-gray-900 tracking-tight mb-4">
          Adopción <span class="text-[#02939E]">Online</span>
        </h2>
        <p class="text-gray-500 max-w-2xl mx-auto text-lg font-light">
          Descubre a los pequeños que están buscando un hogar lleno de amor.
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <router-link 
          v-for="(mascota, index) in mascotas" 
          :key="index" 
          to="/adopcion" 
          class="group relative h-96 w-full rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl hover:shadow-[#02939E]/20 transition-all duration-500 ease-out transform hover:-translate-y-2"
        >
          <div class="absolute top-4 right-4 z-20 bg-white/95 backdrop-blur-sm px-3 py-1.5 rounded-full shadow-sm flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-[#a4ad74] animate-pulse"></div>
            <span class="text-xs font-bold text-gray-700 uppercase tracking-wider">{{ mascota.count }} Disp.</span>
          </div>

          <div class="h-full w-full overflow-hidden">
            <img 
              :src="mascota.image" 
              :alt="mascota.name" 
              class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            >
          </div>
          
          <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/30 to-transparent opacity-70 group-hover:opacity-90 transition-opacity duration-500"></div>

          <div class="absolute bottom-0 left-0 w-full p-8 text-left">
            
            <div class="relative inline-block">
              <h3 class="text-3xl font-serif font-bold text-white mb-1 drop-shadow-md relative z-10">
                {{ mascota.name }}
              </h3>
              <div class="absolute -bottom-2 left-0 h-1 bg-[#a4ad74] w-8 group-hover:w-full transition-all duration-500 ease-out rounded-full"></div>
            </div>

            <div class="h-0 group-hover:h-auto overflow-hidden transition-all duration-500">
                <div class="mt-4 flex items-center gap-2 text-white font-bold text-xs tracking-widest uppercase opacity-0 group-hover:opacity-100 transition-opacity duration-500 delay-100">
                  <span class="text-[#a4ad74]">Adoptar ahora</span> 
                  <span>→</span>
                </div>
            </div>
          </div>
        </router-link>

      </div>

    </div>
  </section>
</template>

<script setup>
import gatoImage from '@/assets/images/gato.png';
import perroImage from '@/assets/images/perro.png';
import hamsterImage from '@/assets/images/hamster.png';
import pecesImage from '@/assets/images/peces.png';

const mascotas = [
  { name: 'Gatos', image: gatoImage, count: 12 },
  { name: 'Perros', image: perroImage, count: 8 },
  { name: 'Hámsters', image: hamsterImage, count: 5 },
  { name: 'Peces', image: pecesImage, count: 15 },
];
</script>