<template>
  <footer class="relative w-full pt-10 pb-4 font-sans overflow-hidden bg-white">
    
    <div class="absolute inset-0 z-0">
      <img 
        :src="footerBg" 
        alt="Fondo decorativo" 
        class="w-full h-full object-fill"
      />
    </div>

    <div class="absolute top-4 left-4 z-0 opacity-50 pointer-events-none">
       <img 
          :src="patitasImage" 
          alt="Huellas decorativas" 
          class="w-24 md:w-32 -rotate-12 grayscale opacity-30"
       />
    </div>

    <div class="relative z-10 px-6 md:px-16 pt-12">
      
      <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6 md:gap-10 items-end">
        
        <div class="flex flex-col space-y-3">
          
          <h3 class="text-xl font-serif font-bold text-gray-800 tracking-wide border-l-4 border-[#02939E] pl-3">
            Contáctanos
          </h3>

          <div class="space-y-2">
            <div class="flex items-center gap-2 group">
              <div class="bg-white p-1.5 rounded-full shadow-sm text-[#02939E]">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5">
                  <path fill-rule="evenodd" d="M1.5 4.5a3 3 0 013-3h1.372c.86 0 1.61.586 1.819 1.42l1.105 4.423a1.875 1.875 0 01-.694 1.955l-1.293.97c-.135.101-.164.249-.126.352a11.285 11.285 0 006.697 6.697c.103.038.25.009.352-.126l.97-1.293a1.875 1.875 0 011.955-.694l4.423 1.105c.834.209 1.42.959 1.42 1.82V19.5a3 3 0 01-3 3h-2.25C8.552 22.5 1.5 15.448 1.5 5.25V4.5z" clip-rule="evenodd" />
                </svg>
              </div>
              <span class="text-gray-700 font-medium text-sm">999-999-99 / 999-999-99</span>
            </div>

            <div class="flex items-center gap-2 group">
              <div class="bg-white p-1.5 rounded-full shadow-sm text-[#02939E]">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5">
                  <path d="M1.5 8.67v8.58a3 3 0 003 3h15a3 3 0 003-3V8.67l-8.928 5.493a3 3 0 01-3.144 0L1.5 8.67z" />
                  <path d="M22.5 6.908V6.75a3 3 0 00-3-3h-15a3 3 0 00-3 3v.158l9.714 5.978a1.5 1.5 0 001.572 0L22.5 6.908z" />
                </svg>
              </div>
              <span class="text-gray-700 font-medium text-sm">contacto@veterinaria.com</span>
            </div>

            <div class="flex items-center gap-2 group">
              <div class="bg-white p-1.5 rounded-full shadow-sm text-[#02939E]">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-3.5 h-3.5">
                  <path fill-rule="evenodd" d="M11.54 22.351l.07.04.028.016a.76.76 0 00.723 0l.028-.015.071-.041a16.975 16.975 0 001.144-.742 19.58 19.58 0 002.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 00-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 002.682 2.282 16.975 16.975 0 001.145.742zM12 13.5a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
                </svg>
              </div>
              <span class="text-gray-700 font-medium text-sm">Av. Principal 123, Chincha</span>
            </div>
          </div>
        </div>

        <div class="flex flex-col items-center md:items-end text-center md:text-right space-y-3 mt-4 md:mt-0">
          
          <h3 class="text-xl font-serif font-bold text-gray-800 tracking-wide">
            Síguenos
          </h3>

          <div class="flex gap-3">
            <a href="#" class="bg-[#02939E] w-10 h-10 rounded-lg flex items-center justify-center shadow-md text-white hover:-translate-y-1 transition-transform duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v2.385z"/></svg>
            </a>
            <a href="#" class="bg-[#02939E] w-10 h-10 rounded-lg flex items-center justify-center shadow-md text-white hover:-translate-y-1 transition-transform duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.85s-.011 3.584-.069 4.85c-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07s-3.584-.012-4.85-.07c-3.252-.148-4.771-1.691-4.919-4.919-.058-1.265-.069-1.645-.069-4.85s.011-3.584.069-4.85c.149-3.225 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.85-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948s.014 3.667.072 4.947c.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072s3.667-.014 4.947-.072c4.358-.2 6.78-2.618 6.98-6.98.059-1.281.073-1.689.073-4.948s-.014-3.667-.072-4.947c-.2-4.358-2.618-6.78-6.98-6.98-1.281-.058-1.689-.072-4.948-.072zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.162 6.162 6.162 6.162-2.759 6.162-6.162-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4s1.791-4 4-4 4 1.79 4 4-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.441 1.441 1.441 1.441-.645 1.441-1.441-.645-1.44-1.441-1.44z"/></svg>
            </a>
            <a href="#" class="bg-[#02939E] w-10 h-10 rounded-lg flex items-center justify-center shadow-md text-white hover:-translate-y-1 transition-transform duration-300">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="white"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.65-1.62-1.1-.04 1.82.01 3.64.01 5.46 0 4.85-3.96 8.79-8.84 8.78-4.89-.01-8.87-3.98-8.86-8.86.01-4.88 3.98-8.85 8.86-8.85 1.2 0 2.4.26 3.52.73v4.25c-2.42-1.62-5.73-.85-7.37 1.69-1.62 2.53-.86 5.86 1.68 7.5 2.53 1.62 5.86.86 7.5-1.68.39-.6.68-1.27.83-1.97.03-1.88.01-3.76.01-5.64.95-.01 1.9-.01 2.85-.02-1.44-1.35-2.32-3.26-2.42-5.29z"/></svg>
            </a>
          </div>
        </div>

      </div>

      <div class="mt-8 text-center border-t border-gray-800/10 pt-4">
        <p class="text-gray-500 text-[10px] font-medium tracking-wide">
          Copyright {{ currentYear }} by Clínica Veterinaria Velit. Todos los derechos reservados.
        </p>
      </div>

    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue';
import patitasImage from '@/assets/images/patitas.svg'; 
import footerBg from '@/assets/images/Fondo_final.png';

const currentYear = computed(() => new Date().getFullYear());
</script>