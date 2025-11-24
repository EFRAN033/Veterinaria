// src/axios.js
import axios from 'axios';
import { useUserStore } from '@/stores/user'; 

const apiClient = axios.create({
  baseURL: '/api', // Usar '/api' para que el proxy de Vite lo intercepte
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const userStore = useUserStore(); 
    const token = userStore.token; 

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; 
      const userStore = useUserStore();
      userStore.clearUser(); 
      // Opcional: Podrías añadir aquí lógica para redirigir al login si tienes un router
    }
    return Promise.reject(error);
  }
);

export default apiClient;