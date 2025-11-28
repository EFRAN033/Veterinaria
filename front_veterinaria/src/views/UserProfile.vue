<template>
  <div class="min-h-screen bg-gray-50 flex flex-col relative overflow-hidden">
    <!-- Decorative Background Elements -->
    <div class="absolute top-0 right-0 w-[500px] h-[500px] bg-[#1BB0B9]/10 rounded-full blur-[100px] pointer-events-none translate-x-1/3 -translate-y-1/3"></div>
    <div class="absolute bottom-0 left-0 w-[500px] h-[500px] bg-[#BEDC74]/20 rounded-full blur-[100px] pointer-events-none -translate-x-1/3 translate-y-1/3"></div>

    <!-- Back Button -->
    <BackButton />

    <!-- Main Content -->
    <main class="flex-grow container mx-auto px-4 sm:px-6 lg:px-8 py-12 relative z-10">
      <div class="max-w-5xl mx-auto">
        
        <!-- Header Section (No Card) -->
        <div class="mb-16 mt-8">
          <h1 class="text-5xl font-serif font-bold text-gray-900 mb-4 tracking-tight">
            Hola, <span class="text-transparent bg-clip-text bg-gradient-to-r from-[#16aeb1] to-[#1BB0B9]">{{ userProfile?.name?.split(' ')[0] || 'Usuario' }}</span>
          </h1>
          <p class="text-xl text-gray-500 font-light max-w-2xl">
            Aquí está toda la información de tu cuenta. Gestiona tus datos personales y revisa tu estado.
          </p>
        </div>

        <div v-if="loading" class="flex justify-center py-20">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#1BB0B9]"></div>
        </div>

        <div v-else-if="error" class="text-red-500 text-lg font-medium mb-8">
          {{ error }}
        </div>

        <div v-else class="grid grid-cols-1 lg:grid-cols-12 gap-12 lg:gap-24">
          
          <!-- Left Column: Main Info -->
          <div class="lg:col-span-7 space-y-12">
            
            <!-- Section: Contact -->
            <div>
              <h3 class="text-sm font-bold text-[#1BB0B9] uppercase tracking-widest mb-8 flex items-center gap-3">
                <span class="w-8 h-[2px] bg-[#1BB0B9]"></span>
                Información de Contacto
              </h3>
              
              <div class="space-y-8 pl-4 border-l-2 border-gray-100">
                <!-- Email -->
                <div class="group">
                  <label class="block text-sm text-gray-400 mb-1">Correo Electrónico</label>
                  <div class="flex items-center gap-4">
                    <span class="text-2xl text-gray-800 font-medium group-hover:text-[#1BB0B9] transition-colors">
                      {{ userProfile?.email || 'No disponible' }}
                    </span>
                  </div>
                </div>

                <!-- Phone -->
                <div class="group">
                  <label class="block text-sm text-gray-400 mb-1">Teléfono</label>
                  <div class="flex items-center gap-4">
                    <span class="text-2xl text-gray-800 font-medium group-hover:text-[#1BB0B9] transition-colors">
                      {{ userProfile?.phone || 'No registrado' }}
                    </span>
                  </div>
                </div>

                <!-- Address -->
                <div class="group">
                  <label class="block text-sm text-gray-400 mb-1">Dirección</label>
                  <div class="flex items-center gap-4">
                    <span class="text-xl text-gray-800 font-medium group-hover:text-[#1BB0B9] transition-colors leading-relaxed">
                      {{ userProfile?.address || 'No registrada' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

          </div>

          <!-- Right Column: Status & Actions -->
          <div class="lg:col-span-5 space-y-12">
            
            <!-- Section: Account -->
            <div>
              <h3 class="text-sm font-bold text-[#1BB0B9] uppercase tracking-widest mb-8 flex items-center gap-3">
                <span class="w-8 h-[2px] bg-[#1BB0B9]"></span>
                Detalles de Cuenta
              </h3>

              <div class="space-y-8">
                <!-- Status Badge (No Card, just clean design) -->
                <div class="flex items-center gap-6">
                  <div class="relative">
                    <div class="w-16 h-16 rounded-2xl flex items-center justify-center transition-colors"
                         :class="userProfile?.is_active ? 'bg-green-50 text-green-600' : 'bg-red-50 text-red-600'">
                      <svg v-if="userProfile?.is_active" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <svg v-else class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                    <!-- Status Dot -->
                    <div class="absolute -top-1 -right-1 w-4 h-4 rounded-full border-2 border-white"
                         :class="userProfile?.is_active ? 'bg-green-500' : 'bg-red-500'"></div>
                  </div>
                  <div>
                    <p class="text-sm text-gray-400 mb-1">Estado</p>
                    <p class="text-xl font-bold text-gray-900">{{ userProfile?.is_active ? 'Activa' : 'Inactiva' }}</p>
                  </div>
                </div>

                <!-- Role & Date -->
                <div class="grid grid-cols-2 gap-8">
                  <div>
                    <label class="block text-sm text-gray-400 mb-2">Rol</label>
                    <p class="text-lg font-semibold text-gray-800 capitalize flex items-center gap-2">
                      <span class="w-2 h-2 rounded-full bg-[#1BB0B9]"></span>
                      {{ userProfile?.role || 'Usuario' }}
                    </p>
                  </div>
                  <div>
                    <label class="block text-sm text-gray-400 mb-2">Miembro desde</label>
                    <p class="text-lg font-semibold text-gray-800">
                      {{ formatDate(userProfile?.created_at) }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Actions (Minimalist Buttons) -->
            <div class="pt-8 border-t border-gray-200/50">
              <div class="flex flex-col gap-4">
                <button class="group flex items-center justify-between w-full py-4 px-2 border-b border-gray-200 hover:border-[#1BB0B9] transition-all">
                  <span class="text-lg font-medium text-gray-600 group-hover:text-[#1BB0B9] transition-colors">Editar Perfil</span>
                  <svg class="w-6 h-6 text-gray-300 group-hover:text-[#1BB0B9] group-hover:translate-x-2 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </button>
                <button class="group flex items-center justify-between w-full py-4 px-2 border-b border-gray-200 hover:border-[#1BB0B9] transition-all">
                  <span class="text-lg font-medium text-gray-600 group-hover:text-[#1BB0B9] transition-colors">Cambiar Contraseña</span>
                  <svg class="w-6 h-6 text-gray-300 group-hover:text-[#1BB0B9] group-hover:translate-x-2 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useUserStore } from '@/stores/user';
import BackButton from '@/components/BackButton.vue';
import Footer from './Footer.vue';

const userStore = useUserStore();
const userProfile = ref(null);
const loading = ref(true);
const error = ref(null);

const formatDate = (dateString) => {
  if (!dateString) return 'Fecha no disponible';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('es-ES', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  }).format(date);
};

onMounted(async () => {
  try {
    loading.value = true;
    await userStore.fetchProfile();
    userProfile.value = userStore.user;
  } catch (e) {
    error.value = 'No se pudo cargar la información del perfil.';
    console.error(e);
  } finally {
    loading.value = false;
  }
});
</script>
