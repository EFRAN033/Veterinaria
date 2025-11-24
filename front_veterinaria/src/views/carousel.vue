<template>
  <section class="w-full py-16 px-4 bg-white border-t border-gray-100 overflow-hidden">
    
    <div class="max-w-7xl mx-auto">
      
      <p class="text-center text-gray-400 text-sm font-bold tracking-[0.2em] uppercase mb-10">
        Trabajamos con las mejores marcas
      </p>

      <div 
        class="relative w-full overflow-hidden group"
        style="mask-image: linear-gradient(to right, transparent, black 10%, black 90%, transparent);"
      >
        
        <div class="flex gap-8 w-max animate-scroll group-hover:paused">
          
          <div 
            v-for="(item, index) in [...carouselItems, ...carouselItems]" 
            :key="index" 
            class="flex-none w-48 h-28"
          >
            <div class="w-full h-full bg-gray-50 rounded-xl border border-gray-100 flex flex-col items-center justify-center cursor-pointer transition-all duration-300 hover:bg-white hover:shadow-lg hover:border-[#02939E]/30 hover:scale-105 group/card">
              
              <div class="opacity-40 group-hover/card:opacity-100 transition-opacity duration-300">
                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-8 h-8 mb-2 mx-auto text-gray-600 group-hover/card:text-[#02939E]">
                    <path fill-rule="evenodd" d="M9.315 7.584C12.195 3.883 16.695 1.5 21.75 1.5a.75.75 0 01.75.75c0 5.056-2.383 9.555-6.084 12.436h.678c2.08 0 3.877 1.466 4.321 3.48l.496 2.232a3.75 3.75 0 01-4.346 4.53l-2.232-.495a4.504 4.504 0 01-3.48-4.322v-.678A13.99 13.99 0 017.584 9.315l-.678.15a4.504 4.504 0 01-4.322-3.48l-.495-2.232a3.75 3.75 0 014.53-4.346l2.232.496c2.014.444 3.48 2.24 3.48 4.321v.678z" clip-rule="evenodd" />
                  </svg>
              </div>

              <span class="text-gray-400 font-bold text-lg group-hover/card:text-gray-800 transition-colors duration-300">
                {{ item.text }}
              </span>
              
            </div>
          </div>

        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';

// Datos de Marcas
const carouselItems = ref([
  { id: 1, text: 'Royal Canin' },
  { id: 2, text: 'Purina' },
  { id: 3, text: 'Hills' },
  { id: 4, text: 'Pedigree' },
  { id: 5, text: 'Bayer' },
  { id: 6, text: 'NexGard' },
  { id: 7, text: 'ProPlan' },
  { id: 8, text: 'Whiskas' },
  { id: 9, text: 'Eukanuba' },
  { id: 10, text: 'Ricocan' },
]);

// ¡Ya no necesitamos lógica JS compleja! Todo lo hace el CSS.
</script>

<style scoped>
/* ANIMACIÓN DE SCROLL INFINITO 
  Mueve el contenido de 0 a -50% (porque duplicamos el contenido)
*/
@keyframes scroll {
  0% {
    transform: translateX(0);
  }
  100% {
    /* Si tienes muchos items, ajusta este valor. 
       Al duplicar la lista, -50% es el punto exacto para el loop perfecto. */
    transform: translateX(-50%);
  }
}

.animate-scroll {
  /* 30s linear infinite: 
    - 30s: Velocidad (más segundos = más lento)
    - linear: Velocidad constante sin acelerones
    - infinite: Nunca para
  */
  animation: scroll 30s linear infinite;
  width: max-content; /* Asegura que los elementos se pongan en fila */
}

/* Pausar la animación al poner el mouse encima (opcional, pero recomendado por UX) */
.paused {
  animation-play-state: paused;
}
</style>