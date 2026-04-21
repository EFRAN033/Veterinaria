<template>
  <div class="h-screen w-full bg-gray-50 flex overflow-hidden font-sans">
    
    <aside 
      class="flex flex-col transition-all duration-300 ease-out relative z-20 shrink-0 bg-[#027a83] text-white"
      :class="sidebarOpen ? 'w-56' : 'w-20'"
    >
      <div class="flex items-center px-5 shrink-0 overflow-hidden whitespace-nowrap mt-10 mb-6">
        <div class="transition-all duration-300">
          <div v-if="sidebarOpen" class="flex flex-col">
            <h1 class="font-black text-2xl tracking-tighter leading-none text-white">
              VET<span class="text-white/75">CLINIC</span>
            </h1>
            <p class="text-[10px] text-white/60 uppercase tracking-widest mt-1.5 font-bold ml-0.5">Clínica Velit</p>
          </div>
          
          <div v-else class="font-black text-xl text-white tracking-tighter mx-auto">
            V
          </div>
        </div>
      </div>

      <nav class="flex-1 px-3 space-y-2 overflow-y-auto custom-scrollbar">
        <router-link 
          v-for="item in navigation" 
          :key="item.name" 
          :to="item.href"
          class="relative flex items-center px-3 py-3.5 rounded-none transition-all duration-200 group overflow-hidden"
          :class="[
            isNavActive(item)
              ? 'bg-white/15 text-white border border-white/25' 
              : 'text-white/85 hover:bg-white/10 hover:text-white'
          ]"
        >
          <div v-if="isNavActive(item)" class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-white rounded-none shadow-[0_0_12px_rgba(255,255,255,0.5)]"></div>

          <component 
            :is="item.icon" 
            class="h-6 w-6 flex-shrink-0 transition-transform duration-300 group-hover:scale-110"
            :class="isNavActive(item) ? 'text-white' : 'text-white/70 group-hover:text-white'"
          />
          
          <span 
            v-if="sidebarOpen" 
            class="ml-3 font-medium text-sm whitespace-nowrap transition-all duration-300"
          >
            {{ item.name }}
          </span>

          <div v-if="!sidebarOpen" class="absolute left-14 bg-[#015a61] text-white text-xs px-3 py-1.5 rounded-none opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-50 shadow-xl border border-white/20 whitespace-nowrap ml-2">
            {{ item.name }}
          </div>
        </router-link>
      </nav>

      <div class="p-3 shrink-0 mb-4">
        <div class="bg-black/15 rounded-none p-1 border border-white/20">
          <button 
            @click="logout" 
            class="flex items-center justify-center w-full px-4 py-2.5 text-white/90 hover:bg-rose-500/20 hover:text-rose-100 rounded-none transition-all duration-200 group"
          >
            <ArrowRightOnRectangleIcon class="h-5 w-5 flex-shrink-0 transition-transform group-hover:-translate-x-1" />
            <span v-if="sidebarOpen" class="ml-3 font-medium text-sm">Cerrar Sesión</span>
          </button>
        </div>
      </div>
    </aside>

    <div 
      class="flex-1 bg-gray-50 flex flex-col relative z-10 transition-all duration-300 rounded-none shadow-none"
    >
      
      <header class="h-20 px-8 flex items-center justify-between bg-white border-b border-gray-200 sticky top-0 z-30 rounded-none">
        
        <div class="flex items-center gap-4">
          <button @click="sidebarOpen = !sidebarOpen" class="p-2 rounded-none text-slate-500 hover:bg-gray-100 hover:text-[#02939E] transition-colors focus:outline-none">
            <Bars3BottomLeftIcon class="h-6 w-6" />
          </button>
          
          <div class="h-6 w-px bg-slate-200 hidden sm:block"></div>
          
          <h2 class="text-lg font-bold text-slate-700 hidden sm:block tracking-tight">
            {{ currentTitle }}
          </h2>
        </div>

        <div class="flex items-center gap-6">
          <div class="hidden md:flex items-center bg-gray-100 px-3 py-2 rounded-none w-64 border border-gray-200 focus-within:border-[#02939E] focus-within:ring-2 focus-within:ring-[#02939E]/20 transition-all">
            <MagnifyingGlassIcon class="h-4 w-4 text-slate-400" />
            <input type="text" placeholder="Buscar..." class="bg-transparent border-none text-xs w-full ml-2 focus:outline-none text-slate-600 placeholder-slate-400" />
          </div>

          <div class="flex items-center gap-3">
            <button type="button" class="relative p-2 text-slate-400 hover:text-[#02939E] hover:bg-[#02939E]/10 rounded-none transition-colors">
              <BellIcon class="h-6 w-6" />
              <span class="absolute top-2 right-2 h-2 w-2 bg-rose-500 rounded-full border-2 border-white"></span>
            </button>
            
            <div class="flex items-center gap-3 pl-3 border-l border-slate-200 cursor-pointer group">
              <div class="text-right hidden lg:block">
                <p class="text-sm font-bold text-slate-700 group-hover:text-[#02939E] transition-colors">Dr. Juan Pérez</p>
                <p class="text-[10px] font-medium text-slate-400 uppercase">Veterinario Jefe</p>
              </div>
              <div class="h-10 w-10 rounded-none bg-[#02939E] p-0.5 shadow-md shadow-[#02939E]/30">
                <div class="h-full w-full rounded-none bg-white flex items-center justify-center overflow-hidden">
                  <span class="font-bold text-[#02939E] text-sm">DR</span>
                </div>
              </div>
              <ChevronDownIcon class="h-3 w-3 text-slate-400 lg:hidden" />
            </div>
          </div>
        </div>
      </header>

      <main class="flex-1 overflow-x-hidden overflow-y-auto p-6 custom-scrollbar">
        <router-view v-slot="{ Component }">
          <transition name="fade-slide" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { 
  Squares2X2Icon, 
  CalendarDaysIcon, 
  ClockIcon, 
  ChartBarIcon,
  ArrowRightOnRectangleIcon,
  Bars3BottomLeftIcon,
  BellIcon,
  MagnifyingGlassIcon,
  ChevronDownIcon
} from '@heroicons/vue/24/outline';

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();
const sidebarOpen = ref(true);

const navigation = [
  { name: 'Dashboard', href: '/veterinario', icon: Squares2X2Icon },
  { name: 'Citas', href: '/veterinario/citas', icon: CalendarDaysIcon },
  { name: 'Calendario', href: '/veterinario/calendar', icon: CalendarDaysIcon },
  { name: 'Historial Clínico', href: '/veterinario/history', icon: ClockIcon },
  { name: 'Análisis', href: '/veterinario/analisis', icon: ChartBarIcon },
];

const isNavActive = (item) => {
  if (item.href === '/veterinario') {
    return route.path === '/veterinario' || route.path === '/veterinario/';
  }
  return route.path === item.href || route.path.startsWith(item.href + '/');
};

const currentTitle = computed(() => route.meta.title || 'Panel General');

const logout = () => {
  userStore.logout();
  router.push('/login');
};
</script>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}

main.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
}
main.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>