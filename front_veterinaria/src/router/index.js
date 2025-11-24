// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';

// 1. Importamos los componentes (Lazy loading es recomendable)
const Main = () => import('../views/Main.vue');
// AGREGADO: Importar el componente de Adopción
// Asegúrate de que la ruta '../views/Onlineadoption.vue' sea la correcta.
// Si está en components, cambia 'views' por 'components'.
const Onlineadoption = () => import('../views/Onlineadoption.vue');

const routes = [
  // Redirección para la ruta raíz
  {
    path: '/',
    redirect: '/home'
  },

  {
    path: '/home',
    name: 'Home',
    component: Main,
    meta: { title: 'Página Principal' },
  },

  // --- NUEVA RUTA AGREGADA ---
  {
    path: '/adopcion',     // Esta es la URL que pusimos en el router-link del Header
    name: 'Adopcion',
    component: Onlineadoption,
    meta: { title: 'Adopción Online' } // Título para la pestaña del navegador
  },
  {
    path: '/petshop',
    name: 'PetShop',
    component: () => import('../views/PetShop.vue'),
    meta: { title: 'Pet Shop' }
  },
  {
    path: '/servicios',
    name: 'Servicios',
    component: () => import('../views/Services.vue'),
    meta: { title: 'Servicios Veterinarios' }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { title: 'Iniciar Sesión' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { title: 'Registrarse' }
  },

  // Ruta para manejar errores 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: { template: `<div class="p-8"><h1 class="font-bold text-2xl">404 - Página No Encontrada</h1><router-link to="/home" class="text-indigo-600">Volver al inicio</router-link></div>` },
    meta: { title: '404 | No Encontrado' }
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior: () => ({ top: 0 })
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ path: '/' });
  } else {
    next();
  }
});

router.afterEach((to) => {
  document.title = to.meta?.title || 'Veterinaria';
});

export default router;