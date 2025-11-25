import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import apiClient from '@/axios';

/**
 * Composable para manejar autenticación
 * @returns {Object} Métodos y estado de autenticación
 */
export const useAuth = () => {
    const router = useRouter();
    const userStore = useUserStore();

    const loading = ref(false);
    const error = ref('');

    /**
     * Maneja errores de autenticación
     * @param {Error} err - Error capturado
     */
    const handleAuthError = (err) => {
        console.error('Auth error:', err);

        if (err.response) {
            switch (err.response.status) {
                case 400:
                    error.value = err.response.data?.message || 'Datos inválidos';
                    break;
                case 401:
                    error.value = 'Credenciales incorrectas';
                    break;
                case 409:
                    error.value = 'Este email ya está registrado';
                    break;
                case 422:
                    error.value = err.response.data?.message || 'Error de validación';
                    break;
                case 500:
                    error.value = 'Error del servidor. Intenta más tarde';
                    break;
                default:
                    error.value = 'Error al procesar la solicitud';
            }
        } else if (err.request) {
            error.value = 'Error de conexión. Verifica tu internet';
        } else {
            error.value = 'Error inesperado. Intenta nuevamente';
        }
    };

    /**
     * Inicia sesión
     * @param {Object} credentials - Email y contraseña
     * @returns {Promise<boolean>} True si fue exitoso
     */
    const login = async (credentials) => {
        try {
            loading.value = true;
            error.value = '';

            const response = await apiClient.post('/auth/login', {
                email: credentials.email,
                password: credentials.password,
            });

            userStore.setToken(response.data.access_token);

            const userRole = userStore.userRole;
            if (userRole === 'veterinario') {
                await router.push('/veterinario');
            } else {
                await router.push('/home');
            }

            return true;
        } catch (err) {
            handleAuthError(err);
            return false;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Registra un nuevo usuario
     * @param {Object} userData - Datos del usuario
     * @returns {Promise<boolean>} True si fue exitoso
     */
    const register = async (userData) => {
        try {
            loading.value = true;
            error.value = '';

            const response = await apiClient.post('/auth/register', {
                name: userData.name,
                email: userData.email,
                password: userData.password,
            });


            await router.push('/login');

            return true;
        } catch (err) {
            handleAuthError(err);
            return false;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Cierra sesión
     */
    const logout = async () => {
        try {
            loading.value = true;

            try {
                await apiClient.post('/auth/logout');
            } catch (err) {
                console.warn('Error al cerrar sesión en el servidor:', err);
            }

            userStore.clearUser();

            await router.push('/');

        } catch (err) {
            console.error('Error al cerrar sesión:', err);
        } finally {
            loading.value = false;
        }
    };

    /**
     * Limpia el mensaje de error
     */
    const clearError = () => {
        error.value = '';
    };

    return {
        loading,
        error,
        login,
        register,
        logout,
        clearError,
    };
};
