<template>
  <header class="absolute top-0 left-0 w-full z-40 bg-transparent">
    <div class="container mx-auto flex items-center justify-between py-4 px-4 md:px-8">
      <!-- Brand -->
      <div class="flex items-center gap-3">
        <!-- Brand removed as requested -->
      </div>

      <!-- Navigation -->
      <nav class="hidden md:flex items-center gap-4">
        <div class="flex items-center gap-4 bg-white/6 backdrop-blur-sm rounded-md px-2 py-1 shadow-sm">
          <router-link to="/servicios" class="flex items-center justify-center px-5 py-3 rounded-md text-white bg-gradient-to-br from-[#16aeb1] to-[#1BB0B9] hover:translate-y-0.5 transform transition-transform duration-150 min-w-[120px] text-base font-medium border border-white/20">
            <span>Servicios</span>
          </router-link>

          <router-link to="/petshop" class="flex items-center justify-center px-5 py-3 rounded-md text-white bg-gradient-to-br from-[#16aeb1] to-[#1BB0B9] hover:translate-y-0.5 transform transition-transform duration-150 min-w-[120px] text-base font-medium border border-white/20">
            <span>Pet Shop</span>
          </router-link>

          <router-link to="/adopcion" class="flex items-center justify-center px-5 py-3 rounded-md text-white bg-gradient-to-br from-[#16aeb1] to-[#1BB0B9] hover:translate-y-0.5 transform transition-transform duration-150 min-w-[120px] text-base font-medium border border-white/20">
            <span>Adopción</span>
          </router-link>
        </div>

        <!-- Auth Buttons (when not logged in) / Account Icon (when logged in) -->
        <div v-if="!isLoggedIn" class="flex items-center gap-3">
          <router-link 
            to="/login" 
            class="px-4 py-2 text-sm font-bold text-[#1BB0B9] hover:text-[#16a0a8] transition-colors"
          >
            Iniciar Sesión
          </router-link>
          <router-link 
            to="/register" 
            class="px-5 py-2.5 bg-gradient-to-r from-[#1BB0B9] to-[#16a0a8] text-white font-bold rounded-lg hover:shadow-lg transition-all text-sm"
          >
            Registrarse
          </router-link>
        </div>

        <a v-else href="#" aria-label="Mi Cuenta" class="flex items-center justify-center bg-[#1BB0B9] text-white rounded-full shadow w-11 h-11 border border-[#169aa0] hover:scale-105 transition-transform">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5 text-white">
            <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z" clip-rule="evenodd" />
          </svg>
        </a>
      </nav>

      <!-- Mobile menu button (simple placeholder) -->
      <div class="md:hidden">
        <button aria-label="Abrir menú" class="p-2 rounded-md text-gray-700 hover:bg-gray-100">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue';

// Estado de autenticación (por ahora hardcodeado, luego se conectará con el store)
const isLoggedIn = ref(false);

// Función para simular login/logout (temporal)
// En producción, esto se manejará con el store de usuario
</script>