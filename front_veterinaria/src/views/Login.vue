<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex flex-col">
    <!-- Simple Header -->
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <div></div>
          <router-link to="/register" class="text-sm font-bold text-gray-600 hover:text-[#1BB0B9] transition-colors">
            ¿No tienes cuenta? <span class="text-[#1BB0B9]">Regístrate</span>
          </router-link>
        </div>
      </div>
    </header>

    <BackButton />

    <!-- Main Content -->
    <main class="flex-1 flex items-center justify-center px-4 py-12">
      <div class="w-full max-w-md">
        <!-- Login Card -->
        <div class="bg-white rounded-3xl shadow-2xl p-8 border border-gray-100 relative overflow-hidden">
          <!-- Decorative blurs -->
          <div class="absolute top-0 right-0 w-32 h-32 bg-[#1BB0B9] rounded-full blur-[80px] opacity-10"></div>
          <div class="absolute bottom-0 left-0 w-24 h-24 bg-[#BEDC74] rounded-full blur-[60px] opacity-10"></div>

          <div class="relative z-10">
            <!-- Icon -->
            <div class="flex justify-center mb-6">
              <div class="bg-gradient-to-br from-[#1BB0B9] to-[#16a0a8] p-4 rounded-2xl shadow-lg">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            </div>

            <!-- Title -->
            <div class="text-center mb-8">
              <h2 class="text-3xl font-serif font-bold text-gray-900 mb-2">Iniciar Sesión</h2>
              <p class="text-gray-500">Accede a tu cuenta de veterinaria</p>
            </div>

            <!-- Error Message -->
            <ErrorMessage 
              v-if="authError" 
              :message="authError" 
              type="error"
              class="mb-6"
              @dismiss="clearAuthError"
            />

            <!-- Login Form -->
            <form @submit.prevent="handleLogin" class="space-y-6">
              <!-- Email Field -->
              <FloatingInput
                v-model="loginForm.email"
                type="email"
                label="Correo Electrónico"
                :error="errors.email"
                required
                @blur="validateField('email')"
              >
                <template #icon>
                  <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                  </svg>
                </template>
              </FloatingInput>

              <!-- Password Field -->
              <FloatingInput
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                label="Contraseña"
                :error="errors.password"
                required
                @blur="validateField('password')"
              >
                <template #icon>
                  <button 
                    type="button"
                    @click="showPassword = !showPassword"
                    class="text-gray-400 hover:text-[#1BB0B9] transition-colors focus:outline-none"
                    :aria-label="showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'"
                  >
                    <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                    </svg>
                  </button>
                </template>
              </FloatingInput>

              <!-- Remember & Forgot -->
              <div class="flex items-center justify-between text-sm">
                <label class="flex items-center gap-2 cursor-pointer">
                  <input type="checkbox" v-model="loginForm.remember" class="w-4 h-4 accent-[#1BB0B9] rounded">
                  <span class="text-gray-600">Recordarme</span>
                </label>
                <a href="#" class="text-[#1BB0B9] font-bold hover:underline">¿Olvidaste tu contraseña?</a>
              </div>

              <!-- Submit Button -->
              <BaseButton
                type="submit"
                variant="primary"
                size="lg"
                :loading="loading"
                :disabled="hasErrors"
                full-width
                loading-text="Iniciando sesión..."
              >
                Iniciar Sesión
              </BaseButton>
            </form>

            <!-- Divider -->
            <div class="relative my-8">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-200"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-4 bg-white text-gray-500">O continúa con</span>
              </div>
            </div>

            <!-- Social Login -->
            <div class="grid grid-cols-2 gap-4">
              <button class="flex items-center justify-center gap-2 py-3 px-4 border-2 border-gray-200 rounded-xl hover:border-[#1BB0B9] hover:bg-[#1BB0B9]/5 transition-all group">
                <svg class="w-5 h-5" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                <span class="text-sm font-bold text-gray-700">Google</span>
              </button>
              <button class="flex items-center justify-center gap-2 py-3 px-4 border-2 border-gray-200 rounded-xl hover:border-[#1BB0B9] hover:bg-[#1BB0B9]/5 transition-all group">
                <svg class="w-5 h-5 text-[#1877F2]" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                </svg>
                <span class="text-sm font-bold text-gray-700">Facebook</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Register Link -->
        <p class="text-center mt-6 text-gray-600">
          ¿No tienes una cuenta? 
          <router-link to="/register" class="text-[#1BB0B9] font-bold hover:underline ml-1">
            Regístrate aquí
          </router-link>
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

const { validateEmail, validateRequired, errors, setError, clearError } = useFormValidation();
const { login, loading, error: authError, clearError: clearAuthError } = useAuth();

const loginForm = ref({
  email: '',
  password: '',
  remember: false
});

const showPassword = ref(false);

const hasErrors = computed(() => {
  return Object.keys(errors.value).length > 0;
});

const validateField = (field) => {
  clearError(field);
  
  if (field === 'email') {
    const error = validateEmail(loginForm.value.email);
    if (error) setError(field, error);
  } else if (field === 'password') {
    const error = validateRequired(loginForm.value.password, 'La contraseña');
    if (error) setError(field, error);
  }
};

const handleLogin = async () => {
  validateField('email');
  validateField('password');
  
  if (hasErrors.value) return;
  
  await login(loginForm.value);
};
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
