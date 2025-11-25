<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { 
  HomeIcon, 
  CalendarIcon, 
  ClockIcon, 
  ChatBubbleLeftRightIcon, 
  ArrowRightOnRectangleIcon 
} from '@heroicons/vue/24/outline';

const router = useRouter();
const userStore = useUserStore();
const sidebarOpen = ref(true);

const navigation = [
  { name: 'Dashboard', href: '/veterinario', icon: HomeIcon },
  { name: 'Calendario', href: '/veterinario/calendar', icon: CalendarIcon },
  { name: 'Historial', href: '/veterinario/history', icon: ClockIcon },
  { name: 'Asistente IA', href: '/veterinario/chat', icon: ChatBubbleLeftRightIcon },
];

const logout = () => {
  userStore.logout();
  router.push('/login');
};
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex">
    <!-- Sidebar -->
    <aside 
      class="bg-indigo-800 text-white transition-all duration-300 ease-in-out flex flex-col"
      :class="sidebarOpen ? 'w-64' : 'w-20'"
    >
      <div class="p-4 flex items-center justify-between h-16 bg-indigo-900">
        <span v-if="sidebarOpen" class="font-bold text-xl tracking-wider">VETERINARIA</span>
        <span v-else class="font-bold text-xl mx-auto">V</span>
        
        <button @click="sidebarOpen = !sidebarOpen" class="text-gray-300 hover:text-white focus:outline-none">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      <nav class="flex-1 px-2 py-4 space-y-2 overflow-y-auto">
        <router-link 
          v-for="item in navigation" 
          :key="item.name" 
          :to="item.href"
          class="flex items-center px-4 py-3 text-gray-300 hover:bg-indigo-700 hover:text-white rounded-md transition-colors group"
          active-class="bg-indigo-900 text-white"
        >
          <component :is="item.icon" class="h-6 w-6 flex-shrink-0" />
          <span v-if="sidebarOpen" class="ml-3 font-medium">{{ item.name }}</span>
          
          <!-- Tooltip for collapsed state -->
          <div v-if="!sidebarOpen" class="absolute left-16 bg-gray-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50 whitespace-nowrap">
            {{ item.name }}
          </div>
        </router-link>
      </nav>

      <div class="p-4 bg-indigo-900">
        <button 
          @click="logout" 
          class="flex items-center w-full px-4 py-2 text-gray-300 hover:bg-indigo-800 hover:text-white rounded-md transition-colors"
        >
          <ArrowRightOnRectangleIcon class="h-6 w-6 flex-shrink-0" />
          <span v-if="sidebarOpen" class="ml-3 font-medium">Cerrar Sesión</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <header class="bg-white shadow-sm z-10">
        <div class="px-6 py-4 flex justify-between items-center">
          <h1 class="text-2xl font-semibold text-gray-800">
            {{ $route.meta.title || 'Panel Veterinario' }}
          </h1>
          <div class="flex items-center space-x-4">
            <span class="text-gray-600">Hola, Doc</span>
            <div class="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-bold">
              V
            </div>
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 p-6">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
