<template>
  <div class="min-h-screen bg-white flex flex-col font-sans">
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div></div> 
          <router-link to="/login" class="text-sm font-bold text-gray-600 hover:text-brand-primary transition-colors flex items-center gap-2">
            <span>¿Ya tienes cuenta?</span>
            <span class="text-brand-primary bg-brand-primary/10 px-3 py-1 rounded-lg">Inicia sesión</span>
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
          
          <div class="absolute top-0 right-0 w-64 h-64 bg-brand-primary rounded-full blur-[100px] opacity-10 pointer-events-none"></div>
          <div class="absolute bottom-0 left-0 w-64 h-64 bg-brand-accentPink rounded-full blur-[100px] opacity-15 pointer-events-none"></div>

          <div class="relative z-10 grid grid-cols-1 lg:grid-cols-2 min-h-[600px]">
            
            <div class="p-6 md:p-8 lg:p-10 flex flex-col justify-center lg:border-r border-gray-100 bg-white">
              
              <div class="mb-8 text-center lg:text-left"> 
                <div class="inline-block bg-gradient-to-br from-brand-accentPink to-brand-primary p-3 rounded-2xl shadow-lg shadow-brand-primary/30 mb-4"> 
                  <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                  </svg>
                </div>
                <h2 class="text-3xl lg:text-4xl font-serif font-bold text-gray-900 mb-2">Crear Cuenta</h2>
                <p class="text-gray-500 text-lg">Únete a nuestra comunidad de amantes de las mascotas.</p>
              </div>

              <ErrorMessage 
                v-if="authError" 
                :message="authError" 
                type="error"
                class="mb-6"
                @dismiss="clearAuthError"
              />

              <form @submit.prevent="handleRegister" class="space-y-5 max-w-lg mx-auto lg:mx-0 w-full"> 
                <FloatingInput
                  v-model="registerForm.name"
                  type="text"
                  label="Nombre Completo"
                  :error="errors.name"
                  required
                  @blur="validateField('name')"
                />

                <FloatingInput
                  v-model="registerForm.email"
                  type="email"
                  label="Correo Electrónico"
                  :error="errors.email"
                  required
                  @blur="validateField('email')"
                />

                <FloatingInput
                  v-model="registerForm.password"
                  :type="showPassword ? 'text' : 'password'"
                  label="Contraseña"
                  :error="errors.password"
                  helper-text="Mínimo 6 caracteres, una mayúscula y un número"
                  required
                  @blur="validateField('password')"
                >
                  <template #icon>
                    <button 
                      type="button"
                      @click="showPassword = !showPassword"
                      class="text-gray-400 hover:text-brand-primary transition-colors outline-none"
                      :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                    >
                      <svg v-if="!showPassword" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                      <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                      </svg>
                    </button>
                  </template>
                </FloatingInput>

                <FloatingInput
                  v-model="registerForm.passwordConfirm"
                  :type="showPasswordConfirm ? 'text' : 'password'"
                  label="Confirmar Contraseña"
                  :error="errors.passwordConfirm"
                  required
                  @blur="validateField('passwordConfirm')"
                >
                  <template #icon>
                    <button 
                      type="button"
                      @click="showPasswordConfirm = !showPasswordConfirm"
                      class="text-gray-400 hover:text-brand-primary transition-colors outline-none"
                      :aria-label="showPasswordConfirm ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                    >
                      <svg v-if="!showPasswordConfirm" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                      </svg>
                      <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                      </svg>
                    </button>
                  </template>
                </FloatingInput>

                <div class="pt-2">
                  <label class="flex items-start gap-3 cursor-pointer group select-none">
                    <div class="relative flex items-center">
                      <input 
                        type="checkbox" 
                        v-model="registerForm.acceptTerms" 
                        required
                        class="peer h-5 w-5 cursor-pointer appearance-none rounded-md border-2 border-gray-300 transition-all checked:border-brand-primary checked:bg-brand-primary"
                      >
                      <svg class="pointer-events-none absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-white opacity-0 peer-checked:opacity-100" width="12" height="12" viewBox="0 0 12 12" fill="none"><path d="M10 3L4.5 8.5L2 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    </div>
                    <span class="text-sm text-gray-500 leading-tight pt-0.5">
                      He leído y acepto los <a href="#" class="text-brand-primary font-bold hover:underline">términos</a> y la <a href="#" class="text-brand-primary font-bold hover:underline">política de privacidad</a>.
                    </span>
                  </label>
                </div>

                <BaseButton
                  type="submit"
                  variant="secondary"
                  size="lg"
                  :loading="loading"
                  :disabled="!registerForm.acceptTerms || hasErrors"
                  full-width
                  loading-text="Creando cuenta..."
                  class="bg-brand-primary hover:bg-brand-dark text-white border-none"
                >
                  Crear mi Cuenta
                </BaseButton>
              </form>
            </div>

            <div class="p-6 md:p-8 lg:p-10 bg-gray-50/80 flex flex-col justify-center relative">
               <div class="absolute inset-0 opacity-[0.03]" style="background-image: radial-gradient(#d60579 1px, transparent 1px); background-size: 20px 20px;"></div>

              <div class="space-y-8 relative z-10 max-w-lg mx-auto lg:mx-0">
                <div>
                  <h3 class="text-2xl font-bold text-gray-900 mb-3">Otras opciones de acceso</h3>
                  <p class="text-gray-600 leading-relaxed">
                    Si prefieres no crear una contraseña nueva, utiliza tus redes sociales para un acceso rápido y seguro.
                  </p>
                </div>

                <div class="space-y-4">
                  <button class="w-full flex items-center justify-center gap-4 py-3.5 px-4 bg-white border-2 border-gray-200 rounded-xl hover:border-brand-accentPink hover:bg-gray-50 transition-all group duration-300">
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
                      <div class="w-10 h-10 bg-brand-primary/10 rounded-full flex items-center justify-center text-brand-primary">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                      </div>
                      <div>
                        <p class="font-bold text-gray-900">Historial Digital</p>
                        <p class="text-xs text-gray-500">Accede a las recetas de tu mascota</p>
                      </div>
                    </div>
                    
                    <div class="flex items-center gap-4 bg-white p-4 rounded-xl border border-gray-100 shadow-sm">
                      <div class="w-10 h-10 bg-brand-medium/20 rounded-full flex items-center justify-center text-brand-dark">
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
import { ref, computed } from 'vue';
import Footer from './Footer.vue';
import BackButton from '@/components/BackButton.vue';
import FloatingInput from '@/components/FloatingInput.vue';
import BaseButton from '@/components/BaseButton.vue';
import ErrorMessage from '@/components/ErrorMessage.vue';
import { useFormValidation } from '@/composables/useFormValidation';
import { useAuth } from '@/composables/useAuth';

const { validateEmail, validatePassword, validateRequired, validateMatch, errors, setError, clearError } = useFormValidation();
const { register, loading, error: authError, clearError: clearAuthError } = useAuth();

const registerForm = ref({
  name: '',
  email: '',
  password: '',
  passwordConfirm: '',
  acceptTerms: false
});

const showPassword = ref(false);
const showPasswordConfirm = ref(false);

const hasErrors = computed(() => {
  return Object.keys(errors.value).length > 0;
});

const validateField = (field) => {
  clearError(field);
  
  if (field === 'name') {
    const error = validateRequired(registerForm.value.name, 'El nombre');
    if (error) setError(field, error);
  } else if (field === 'email') {
    const error = validateEmail(registerForm.value.email);
    if (error) setError(field, error);
  } else if (field === 'password') {
    const error = validatePassword(registerForm.value.password);
    if (error) setError(field, error);
    if (registerForm.value.passwordConfirm) {
      validateField('passwordConfirm');
    }
  } else if (field === 'passwordConfirm') {
    const error = validateMatch(
      registerForm.value.password,
      registerForm.value.passwordConfirm,
      'Las contraseñas'
    );
    if (error) setError(field, error);
  }
};

const handleRegister = async () => {
  validateField('name');
  validateField('email');
  validateField('password');
  validateField('passwordConfirm');
  
  if (hasErrors.value) return;
  
  await register(registerForm.value);
};
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>