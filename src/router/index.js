// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';

// Solo necesitamos importar Main, ya que es el componente principal de la vista.
const Main = () => import('../views/Main.vue');

const routes = [
  // Redirección para la ruta raíz
  { 
    path: '/', 
    redirect: '/home' 
  }, 
  
  // --- RUTA 'HOME' SIMPLIFICADA Y CORREGIDA ---
  // Se ha eliminado por completo la propiedad 'children' y la importación de 'HeroSection'
  {
    path: '/home',
    name: 'Home',
    component: Main, // Simplemente le decimos que renderice el componente Main.
    meta: { title: 'Página Principal' },
  },

  // Ruta para manejar errores 404 (página no encontrada)
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

// Los 'navigation guards' se mantienen igual, no son el problema.
router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ path: '/' });
  } else {
    next();
  }
});

router.afterEach((to) => {
  document.title = to.meta?.title || 'Veterinaria'; // Título por defecto
});

export default router;