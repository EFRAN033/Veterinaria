<template>
  <div class="min-h-screen bg-white flex flex-col font-sans">
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div></div> <router-link to="/login" class="text-sm font-bold text-gray-600 hover:text-[#1BB0B9] transition-colors flex items-center gap-2">
            <span>¿Ya tienes cuenta?</span>
            <span class="text-[#1BB0B9] bg-[#1BB0B9]/10 px-3 py-1 rounded-lg">Inicia sesión</span>
          </router-link>
        </div>
      </div>
    </header>

    <div class="container mx-auto px-4 py-6">
      <BackButton />
    </div>

    <main class="flex-1 flex items-center justify-center px-4 pb-12">
      <div class="w-full max-w-6xl">
        
        <div class="bg-white rounded-[2.5rem] shadow-2xl border border-gray-100 relative overflow-hidden">
          
          <div class="absolute top-0 right-0 w-64 h-64 bg-[#1BB0B9] rounded-full blur-[100px] opacity-10 pointer-events-none"></div>
          <div class="absolute bottom-0 left-0 w-64 h-64 bg-[#BEDC74] rounded-full blur-[100px] opacity-10 pointer-events-none"></div>

          <div class="relative z-10 grid grid-cols-1 lg:grid-cols-2 min-h-[600px]">
            
            <div class="p-8 md:p-12 lg:p-16 flex flex-col justify-center lg:border-r border-gray-100 bg-white">
              
              <div class="mb-10 text-center lg:text-left">
                <div class="inline-block bg-gradient-to-br from-[#BEDC74] to-[#a8c965] p-3 rounded-2xl shadow-lg shadow-[#BEDC74]/30 mb-6">
                  <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                </div>
                <h2 class="text-3xl lg:text-4xl font-serif font-bold text-gray-900 mb-2">Crear Cuenta</h2>
                <p class="text-gray-500 text-lg">Únete a nuestra comunidad de amantes de las mascotas.</p>
              </div>

              <form @submit.prevent="handleRegister" class="space-y-6 max-w-lg mx-auto lg:mx-0 w-full">
                <div class="group relative">
                  <input 
                    type="text" 
                    v-model="registerForm.name" 
                    placeholder=" " 
                    required
                    class="floating-input peer"
                  />
                  <label class="floating-label">Nombre Completo</label>
                </div>

                <div class="group relative">
                  <input 
                    type="email" 
                    v-model="registerForm.email" 
                    placeholder=" " 
                    required
                    class="floating-input peer"
                  />
                  <label class="floating-label">Correo Electrónico</label>
                </div>

                <div>
                  <div class="group relative">
                    <input 
                      :type="showPassword ? 'text' : 'password'" 
                      v-model="registerForm.password" 
                      placeholder=" " 
                      required
                      minlength="6"
                      class="floating-input peer"
                    />
                    <label class="floating-label">Contraseña</label>
                    <button 
                      type="button"
                      @click="showPassword = !showPassword"
                      class="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-[#1BB0B9] transition-colors outline-none"
                    >
                      <svg v-if="!showPassword" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                      <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                      </svg>
                    </button>
                  </div>
                  <p class="text-xs text-gray-400 mt-2 ml-1 flex items-center gap-1">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
                    Mínimo 6 caracteres
                  </p>
                </div>

                <div class="pt-2">
                  <label class="flex items-start gap-3 cursor-pointer group select-none">
                    <div class="relative flex items-center">
                      <input 
                        type="checkbox" 
                        v-model="registerForm.acceptTerms" 
                        required
                        class="peer h-5 w-5 cursor-pointer appearance-none rounded-md border-2 border-gray-300 transition-all checked:border-[#1BB0B9] checked:bg-[#1BB0B9]"
                      >
                      <svg class="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-white opacity-0 peer-checked:opacity-100" width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M10 3L4.5 8.5L2 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                    <span class="text-sm text-gray-500 leading-tight pt-0.5">
                      He leído y acepto los <a href="#" class="text-[#1BB0B9] font-bold hover:underline">términos</a> y la <a href="#" class="text-[#1BB0B9] font-bold hover:underline">política de privacidad</a>.
                    </span>
                  </label>
                </div>

                <button 
                  type="submit"
                  :disabled="!registerForm.acceptTerms"
                  class="w-full py-4 bg-gradient-to-r from-[#BEDC74] to-[#a8c965] text-white font-bold text-lg rounded-xl hover:shadow-xl hover:shadow-[#BEDC74]/30 transition-all transform hover:-translate-y-0.5 active:translate-y-0 active:scale-95 flex items-center justify-center gap-2 group disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none disabled:shadow-none"
                >
                  <span>Crear mi Cuenta</span>
                  <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </button>
              </form>
            </div>

            <div class="p-8 md:p-12 lg:p-16 bg-gray-50/80 flex flex-col justify-center relative">
               <div class="absolute inset-0 opacity-[0.03]" style="background-image: radial-gradient(#1BB0B9 1px, transparent 1px); background-size: 20px 20px;"></div>

              <div class="space-y-8 relative z-10 max-w-lg mx-auto lg:mx-0">
                <div>
                  <h3 class="text-2xl font-bold text-gray-900 mb-3">Otras opciones de acceso</h3>
                  <p class="text-gray-600 leading-relaxed">
                    Si prefieres no crear una contraseña nueva, utiliza tus redes sociales para un acceso rápido y seguro.
                  </p>
                </div>

                <div class="space-y-4">
                  <button class="w-full flex items-center justify-center gap-4 py-3.5 px-4 bg-white border-2 border-gray-200 rounded-xl hover:border-[#BEDC74] hover:bg-gray-50 transition-all group duration-300">
                    <img src="https://www.svgrepo.com/show/475656/google-color.svg" class="w-6 h-6" alt="Google">
                    <span class="text-gray-700 font-bold group-hover:text-gray-900">Registrarse con Google</span>
                  </button>
                  
                  <button class="w-full flex items-center justify-center gap-4 py-3.5 px-4 bg-[#1877F2] border-2 border-[#1877F2] rounded-xl hover:bg-[#166fe5] transition-all text-white shadow-md shadow-blue-500/20">
                    <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                    </svg>
                    <span class="font-bold">Registrarse con Facebook</span>
                  </button>
                </div>

                <div class="pt-8 border-t border-gray-200">
                  <h4 class="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">Beneficios de tu cuenta</h4>
                  <div class="grid gap-4">
                    <div class="flex items-center gap-4 bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
                      <div class="w-10 h-10 bg-[#1BB0B9]/10 rounded-full flex items-center justify-center text-[#1BB0B9]">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                      </div>
                      <div>
                        <p class="font-bold text-gray-900">Historial Digital</p>
                        <p class="text-xs text-gray-500">Accede a las recetas de tu mascota</p>
                      </div>
                    </div>
                    
                    <div class="flex items-center gap-4 bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
                      <div class="w-10 h-10 bg-[#BEDC74]/20 rounded-full flex items-center justify-center text-[#1a5f63]">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                      </div>
                      <div>
                        <p class="font-bold text-gray-900">Recordatorios</p>
                        <p class="text-xs text-gray-500">Alertas de vacunas y citas</p>
                      </div>
                    </div>
                  </div>
                </div>

              </div>
            </div>
          </div>
        </div>

        <p class="text-center mt-8 text-gray-500 text-sm">
          Al registrarte, aceptas nuestros términos de servicio.
        </p>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import Footer from './Footer.vue';
import BackButton from '@/components/BackButton.vue';

const registerForm = ref({
  name: '',
  email: '',
  password: '',
  acceptTerms: false
});

const showPassword = ref(false);

const handleRegister = () => {
  console.log('Register:', registerForm.value);
  // Simulación
  alert('Procesando registro...');
};
</script>

<style scoped>
/* Estilos mejorados para Inputs Flotantes */
.floating-input {
  @apply block px-4 pb-2.5 pt-5 w-full text-gray-900 bg-gray-50 border-2 border-gray-100 rounded-xl appearance-none 
  focus:outline-none focus:ring-4 focus:ring-[#1BB0B9]/10 focus:border-[#1BB0B9] focus:bg-white transition-all duration-300;
}

.floating-label {
  @apply absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] left-4 
  peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 peer-focus:text-[#1BB0B9] pointer-events-none font-bold;
}
</style>