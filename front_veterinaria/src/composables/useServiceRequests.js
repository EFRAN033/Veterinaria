/**
 * Composable for Service Requests
 * Handles API calls for service request operations
 */
import { ref } from 'vue';
import apiClient from '@/axios';

export const useServiceRequests = () => {
    const loading = ref(false);
    const error = ref('');

    /**
     * Create a new service request
     * @param {Object} requestData - Service request data
     * @returns {Promise<Object>} Created service request
     */
    const createServiceRequest = async (requestData) => {
        try {
            loading.value = true;
            error.value = '';

            const response = await apiClient.post('/v1/service-requests', requestData);
            return response.data;
        } catch (err) {
            console.error('Error creating service request:', err);
            error.value = err.response?.data?.detail || 'Error al enviar solicitud de servicio';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Get all service requests for current user
     * @returns {Promise<Array>} User's service requests
     */
    const getMyRequests = async () => {
        try {
            loading.value = true;
            error.value = '';

            const response = await apiClient.get('/v1/service-requests/my-requests');
            return response.data;
        } catch (err) {
            console.error('Error fetching my requests:', err);
            error.value = err.response?.data?.detail || 'Error al obtener solicitudes';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Get all service requests (veterinarian only)
     * @param {Object} filters - Optional filters
     * @returns {Promise<Array>} All service requests
     */
    const getAllRequests = async (filters = {}) => {
        try {
            loading.value = true;
            error.value = '';

            const response = await apiClient.get(`/v1/service-requests`, { params: filters });
            return response.data;
        } catch (err) {
            console.error('Error fetching all requests:', err);
            error.value = err.response?.data?.detail || 'Error al obtener solicitudes';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Get a specific service request by ID
     * @param {number} requestId - Request ID
     * @returns {Promise<Object>} Service request
     */
    const getRequestById = async (requestId) => {
        try {
            loading.value = true;
            error.value = '';

            const response = await apiClient.get(`/v1/service-requests/${requestId}`);
            return response.data;
        } catch (err) {
            console.error('Error fetching request:', err);
            error.value = err.response?.data?.detail || 'Error al obtener solicitud';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Update a service request (veterinarian only)
     * @param {number} requestId - Request ID
     * @param {Object} updateData - Update data
     * @returns {Promise<Object>} Updated service request
     */
    const updateRequest = async (requestId, updateData) => {
        try {
            loading.value = true;
            error.value = '';

            const response = await apiClient.patch(`/v1/service-requests/${requestId}`, updateData);
            return response.data;
        } catch (err) {
            console.error('Error updating request:', err);
            error.value = err.response?.data?.detail || 'Error al actualizar solicitud';
            throw err;
        } finally {
            loading.value = false;
        }
    };

    /**
     * Clear error message
     */
    const clearError = () => {
        error.value = '';
    };

    return {
        loading,
        error,
        createServiceRequest,
        getMyRequests,
        getAllRequests,
        getRequestById,
        updateRequest,
        clearError
    };
};
