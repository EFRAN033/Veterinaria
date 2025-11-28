
import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';

const Main = () => import('../views/Main.vue');
const Onlineadoption = () => import('../views/Onlineadoption.vue');

const routes = [
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

  {
    path: '/veterinario',
    component: () => import('../layouts/VetLayout.vue'),
    meta: { requiresAuth: true, title: 'Panel Veterinario' },
    children: [
      {
        path: '',
        name: 'VetDashboard',
        component: () => import('../views/veterinario/VetDashboard.vue'),
        meta: { title: 'Veterinario - Dashboard' }
      },
      {
        path: 'calendar',
        name: 'VetCalendar',
        component: () => import('../views/veterinario/VetCalendar.vue'),
        meta: { title: 'Veterinario - Calendario' }
      },
      {
        path: 'history',
        name: 'VetHistory',
        component: () => import('../views/veterinario/VetHistory.vue'),
        meta: { title: 'Veterinario - Historial' }
      },
      {
        path: 'chat',
        name: 'VetChat',
        component: () => import('../views/veterinario/VetChat.vue'),
        meta: { title: 'Veterinario - Asistente IA' }
      }
    ]
  },

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
    next({ path: '/login' });
    return;
  }

  // Restrict veterinarian from accessing user portal
  if (userStore.isLoggedIn && userStore.userRole === 'veterinario' && !to.path.startsWith('/veterinario')) {
    next({ path: '/veterinario' });
    return;
  }

  if (to.path.startsWith('/veterinario')) {
    if (!userStore.isLoggedIn) {
      next({ path: '/login' });
      return;
    }
    if (userStore.userRole !== 'veterinario') {
      next({ path: '/home' });
      return;
    }
  }

  next();
});

router.afterEach((to) => {
  document.title = to.meta?.title || 'Veterinaria';
});

export default router;