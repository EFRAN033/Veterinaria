<template>
  <Disclosure as="header" class="absolute top-0 left-0 w-full z-40 bg-transparent" v-slot="{ open }">
    <div class="container mx-auto flex items-center justify-between py-4 px-4 md:px-8">
      <div class="flex items-center gap-3">
        </div>

      <nav class="hidden md:flex items-center gap-4">
        <div class="flex items-center gap-4 bg-white/6 backdrop-blur-sm rounded-md px-2 py-1 shadow-sm">
          <router-link 
            to="/servicios" 
            class="flex items-center justify-center px-5 py-3 rounded-md text-white bg-gradient-to-br from-[#16aeb1] to-[#1BB0B9] hover:translate-y-0.5 transform transition-transform duration-150 min-w-[120px] text-base font-medium border border-white/20"
            aria-label="Ir a servicios"
          >
            <span>Servicios</span>
          </router-link>

          <router-link 
            to="/petshop" 
            class="flex items-center justify-center px-5 py-3 rounded-md text-white bg-gradient-to-br from-[#16aeb1] to-[#1BB0B9] hover:translate-y-0.5 transform transition-transform duration-150 min-w-[120px] text-base font-medium border border-white/20"
            aria-label="Ir a pet shop"
          >
            <span>Pet Shop</span>
          </router-link>

          <router-link 
            to="/adopcion" 
            class="flex items-center justify-center px-5 py-3 rounded-md text-white bg-gradient-to-br from-[#16aeb1] to-[#1BB0B9] hover:translate-y-0.5 transform transition-transform duration-150 min-w-[120px] text-base font-medium border border-white/20"
            aria-label="Ir a adopción"
          >
            <span>Adopción</span>
          </router-link>
        </div>

        <div v-if="!userStore.isLoggedIn && isHomePage" class="flex items-center gap-3">
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

        <Menu v-else-if="userStore.isLoggedIn" as="div" class="relative">
          <MenuButton 
            class="flex items-center justify-center bg-[#1BB0B9] text-white rounded-full shadow w-11 h-11 border border-[#169aa0] hover:scale-105 transition-transform focus:outline-none focus:ring-2 focus:ring-[#1BB0B9] focus:ring-offset-2"
            aria-label="Menú de usuario"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5 text-white">
              <path fill-rule="evenodd" d="M7.5 6a4.5 4.5 0 119 0 4.5 4.5 0 01-9 0zM3.751 20.105a8.25 8.25 0 0116.498 0 .75.75 0 01-.437.695A18.683 18.683 0 0112 22.5c-2.786 0-5.433-.608-7.812-1.7a.75.75 0 01-.437-.695z" clip-rule="evenodd" />
            </svg>
          </MenuButton>

          <transition
            enter-active-class="transition duration-100 ease-out"
            enter-from-class="transform scale-95 opacity-0"
            enter-to-class="transform scale-100 opacity-100"
            leave-active-class="transition duration-75 ease-in"
            leave-from-class="transform scale-100 opacity-100"
            leave-to-class="transform scale-95 opacity-0"
          >
            <MenuItems class="absolute right-0 mt-0 w-48 origin-top-right rounded-xl bg-white shadow-xl ring-1 ring-black ring-opacity-5 focus:outline-none z-50 overflow-hidden space-y-2">
              
              <div class="px-4 py-2 bg-gray-50 border-b border-gray-200">
                <p class="text-sm font-bold text-gray-800 truncate leading-snug mb-0">{{ userStore.userShortName }}</p>
                <p class="text-[11px] text-gray-500 truncate leading-tight mb-0">{{ userStore.userEmail }}</p>
              </div>
              
              <div>
                <MenuItem v-slot="{ active }">
                  <router-link
                    to="/profile"
                    :class="[
                      active ? 'bg-[#1BB0B9]/10 text-[#169aa0]' : 'text-gray-700',
                      'block w-full rounded-md px-3 py-2 text-sm transition-colors text-left font-medium'
                    ]"
                  >
                    Mi Perfil
                  </router-link>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <router-link
                    to="/appointments"
                    :class="[
                      active ? 'bg-[#1BB0B9]/10 text-[#169aa0]' : 'text-gray-700',
                      'block w-full rounded-md px-3 py-2 text-sm transition-colors text-left font-medium'
                    ]"
                  >
                    Mis Citas
                  </router-link>
                </MenuItem>
              </div>

              <div class="p-1 border-t border-gray-100">
                <MenuItem v-slot="{ active }">
                  <button
                    @click="handleLogout"
                    :class="[
                      active ? 'bg-red-50 text-red-600' : 'text-red-500',
                      'block w-full rounded-md px-3 py-2 text-sm font-medium transition-colors text-left'
                    ]"
                  >
                    Cerrar Sesión
                  </button>
                </MenuItem>
              </div>
            </MenuItems>
          </transition>
        </Menu>
      </nav>

      <div class="md:hidden">
        <DisclosureButton 
          class="p-2 rounded-md text-gray-700 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-[#1BB0B9]"
          aria-label="Abrir menú de navegación"
        >
          <svg v-if="!open" xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </DisclosureButton>
      </div>
    </div>

    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <DisclosurePanel class="md:hidden bg-white shadow-lg rounded-b-2xl">
        <div class="px-4 py-4 space-y-2">
          <div v-if="userStore.isLoggedIn" class="pb-3 mb-3 border-b border-gray-200">
            <p class="text-sm font-medium text-gray-900">{{ userStore.userShortName }}</p>
            <p class="text-xs text-gray-500">{{ userStore.userEmail }}</p>
          </div>

          <router-link 
            to="/servicios" 
            class="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100 font-medium transition-colors"
          >
            Servicios
          </router-link>
          <router-link 
            to="/petshop" 
            class="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100 font-medium transition-colors"
          >
            Pet Shop
          </router-link>
          <router-link 
            to="/adopcion" 
            class="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100 font-medium transition-colors"
          >
            Adopción
          </router-link>

          <div v-if="!userStore.isLoggedIn && isHomePage" class="pt-3 mt-3 border-t border-gray-200 space-y-2">
            <router-link 
              to="/login" 
              class="block px-4 py-3 rounded-lg text-center text-[#1BB0B9] font-bold hover:bg-[#1BB0B9]/5 transition-colors"
            >
              Iniciar Sesión
            </router-link>
            <router-link 
              to="/register" 
              class="block px-4 py-3 rounded-lg text-center bg-gradient-to-r from-[#1BB0B9] to-[#16a0a8] text-white font-bold hover:shadow-lg transition-all"
            >
              Registrarse
            </router-link>
          </div>

          <div v-else-if="userStore.isLoggedIn" class="pt-3 mt-3 border-t border-gray-200 space-y-2">
            <router-link 
              to="/profile" 
              class="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100 font-medium transition-colors"
            >
              Mi Perfil
            </router-link>
            <router-link 
              to="/appointments" 
              class="block px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100 font-medium transition-colors"
            >
              Mis Citas
            </router-link>
            <button
              @click="handleLogout"
              class="block w-full text-left px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 font-medium transition-colors"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      </DisclosurePanel>
    </transition>
  </Disclosure>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Disclosure, DisclosureButton, DisclosurePanel, Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue';
import { useUserStore } from '@/stores/user';
import { useAuth } from '@/composables/useAuth';

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const { logout } = useAuth();

const isHomePage = computed(() => {
  return route.path === '/' || route.path === '/home';
});

const handleLogout = async () => {
  await logout();
  router.push('/');
};
</script>

<style scoped>
</style>