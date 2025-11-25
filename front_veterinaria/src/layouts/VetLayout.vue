<template>
  <div class="h-screen w-full bg-indigo-900 flex overflow-hidden font-sans">
    
    <aside 
      class="flex flex-col transition-all duration-300 ease-out relative z-20"
      :class="sidebarOpen ? 'w-56' : 'w-20'"
    >
      <div class="flex items-center px-5 shrink-0 overflow-hidden whitespace-nowrap mt-10 mb-6">
        <div class="transition-all duration-300 text-white">
          <div v-if="sidebarOpen" class="flex flex-col">
            <h1 class="font-black text-2xl tracking-tighter leading-none">
              VET<span class="text-indigo-300">CLINIC</span>
            </h1>
            <p class="text-[10px] text-indigo-400 uppercase tracking-widest mt-1.5 font-bold ml-0.5">Sistema Pro</p>
          </div>
          
          <div v-else class="font-black text-xl text-indigo-300 tracking-tighter mx-auto">
            V
          </div>
        </div>
      </div>

      <nav class="flex-1 px-3 space-y-2 overflow-y-auto custom-scrollbar">
        <router-link 
          v-for="item in navigation" 
          :key="item.name" 
          :to="item.href"
          class="relative flex items-center px-3 py-3.5 rounded-xl transition-all duration-200 group overflow-hidden"
          :class="[
            $route.path === item.href 
              ? 'bg-indigo-700/50 text-white shadow-lg shadow-indigo-900/20' 
              : 'text-indigo-200 hover:bg-indigo-800/50 hover:text-white'
          ]"
        >
          <div v-if="$route.path === item.href" class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-indigo-400 rounded-r-full shadow-[0_0_10px_rgba(129,140,248,0.6)]"></div>

          <component 
            :is="item.icon" 
            class="h-6 w-6 flex-shrink-0 transition-transform duration-300 group-hover:scale-110"
            :class="$route.path === item.href ? 'text-indigo-300' : 'text-indigo-400 group-hover:text-white'"
          />
          
          <span 
            v-if="sidebarOpen" 
            class="ml-3 font-medium text-sm whitespace-nowrap transition-all duration-300"
          >
            {{ item.name }}
          </span>

          <div v-if="!sidebarOpen" class="absolute left-14 bg-slate-800 text-white text-xs px-3 py-1.5 rounded-md opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-50 shadow-xl border border-slate-700 whitespace-nowrap ml-2">
            {{ item.name }}
          </div>
        </router-link>
      </nav>

      <div class="p-3 shrink-0 mb-4">
        <div class="bg-indigo-950/30 rounded-xl p-1 border border-indigo-800/50">
          <button 
            @click="logout" 
            class="flex items-center justify-center w-full px-4 py-2.5 text-indigo-300 hover:bg-rose-500/10 hover:text-rose-400 rounded-lg transition-all duration-200 group"
          >
            <ArrowRightOnRectangleIcon class="h-5 w-5 flex-shrink-0 transition-transform group-hover:-translate-x-1" />
            <span v-if="sidebarOpen" class="ml-3 font-medium text-sm">Cerrar Sesión</span>
          </button>
        </div>
      </div>
    </aside>

    <div 
      class="flex-1 bg-slate-50 flex flex-col relative z-10 transition-all duration-300"
      :class="sidebarOpen ? 'rounded-tl-[40px] shadow-[-10px_-10px_30px_rgba(0,0,0,0.2)]' : 'rounded-none'"
    >
      
      <header class="h-20 px-8 flex items-center justify-between bg-white/80 backdrop-blur-md sticky top-0 z-30 border-b border-slate-200/60" :class="sidebarOpen ? 'rounded-tl-[40px]' : ''">
        
        <div class="flex items-center gap-4">
          <button @click="sidebarOpen = !sidebarOpen" class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 hover:text-indigo-600 transition-colors focus:outline-none">
            <Bars3BottomLeftIcon class="h-6 w-6" />
          </button>
          
          <div class="h-6 w-px bg-slate-200 hidden sm:block"></div>
          
          <h2 class="text-lg font-bold text-slate-700 hidden sm:block tracking-tight">
            {{ currentTitle }}
          </h2>
        </div>

        <div class="flex items-center gap-6">
          <div class="hidden md:flex items-center bg-slate-100 px-3 py-2 rounded-full w-64 border border-slate-200 focus-within:border-indigo-300 focus-within:ring-2 focus-within:ring-indigo-100 transition-all">
            <MagnifyingGlassIcon class="h-4 w-4 text-slate-400" />
            <input type="text" placeholder="Buscar..." class="bg-transparent border-none text-xs w-full ml-2 focus:outline-none text-slate-600 placeholder-slate-400" />
          </div>

          <div class="flex items-center gap-3">
            <button class="relative p-2 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-full transition-colors">
              <BellIcon class="h-6 w-6" />
              <span class="absolute top-2 right-2 h-2 w-2 bg-rose-500 rounded-full border-2 border-white"></span>
            </button>
            
            <div class="flex items-center gap-3 pl-3 border-l border-slate-200 cursor-pointer group">
              <div class="text-right hidden lg:block">
                <p class="text-sm font-bold text-slate-700 group-hover:text-indigo-700 transition-colors">Dr. Juan Pérez</p>
                <p class="text-[10px] font-medium text-slate-400 uppercase">Veterinario Jefe</p>
              </div>
              <div class="h-10 w-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 p-0.5 shadow-md shadow-indigo-200">
                <div class="h-full w-full rounded-full bg-white flex items-center justify-center overflow-hidden">
                  <span class="font-bold text-indigo-700 text-sm">DR</span>
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
  ChatBubbleLeftRightIcon, 
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
  { name: 'Calendario', href: '/veterinario/calendar', icon: CalendarDaysIcon },
  { name: 'Historial Clínico', href: '/veterinario/history', icon: ClockIcon },
  { name: 'Asistente IA', href: '/veterinario/chat', icon: ChatBubbleLeftRightIcon },
];

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
</style>