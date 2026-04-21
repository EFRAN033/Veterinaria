import { ref } from 'vue';
import apiClient from '@/axios';

export const usePets = () => {
    const loading = ref(false);
    const error = ref('');

    /**
     * Get all pets for a specific user
     * @param {number} userId - User ID
     * @returns {Promise<Array>} List of pets
     */
    const getPetsByUserId = async (userId) => {
        try {
            loading.value = true;
            error.value = '';

            const response = await apiClient.get(`/v1/pets/user/${userId}`);
            return response.data;
        } catch (err) {
            console.error('Error fetching user pets:', err);
            error.value = err.response?.data?.detail || 'Error al obtener mascotas';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    const createPet = async (payload) => {
        try {
            loading.value = true;
            error.value = '';
            const response = await apiClient.post('/v1/pets/', payload);
            return response.data;
        } catch (err) {
            console.error('Error creating pet:', err);
            error.value = err.response?.data?.detail || 'Error al registrar mascota';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    const updatePet = async (petId, payload) => {
        try {
            loading.value = true;
            error.value = '';
            const response = await apiClient.patch(`/v1/pets/${petId}`, payload);
            return response.data;
        } catch (err) {
            console.error('Error updating pet:', err);
            error.value = err.response?.data?.detail || 'Error al actualizar mascota';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    return {
        loading,
        error,
        getPetsByUserId,
        createPet,
        updatePet,
    };
};
