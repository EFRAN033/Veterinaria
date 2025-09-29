// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

// --- Vistas a Mantener ---
const Main = () => import('../views/Main.vue') // Asumiendo que están en la carpeta 'views'
const HeroSection = () => import('../views/HeroSection.vue') // Asumiendo que están en la carpeta 'views'

const routes = [
  // Redirección por defecto
  { path: '/', redirect: '/home' }, 
  
  // Ruta principal
  {
    path: '/home',
    name: 'Home',
    component: Main,
    meta: { title: 'Página Principal' },
    children: [
      {
        path: 'hero', // Ruta anidada: /home/hero
        name: 'Hero',
        component: HeroSection,
        meta: { title: 'Sección Hero' }
      }
    ]
  },

  // Ruta para páginas no encontradas (404)
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: { template: `<div class="p-8"><h1 class="font-bold text-2xl">404 - No Encontrado</h1><router-link to="/home" class="text-indigo-600">Volver al inicio</router-link></div>` },
    meta: { title: '404 | No Encontrado' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

// Guardián de navegación
router.beforeEach((to, from, next) => {
  const userStore = useUserStore() 
  
  // La lógica de autenticación se mantiene, pero si el usuario no está logueado,
  // la redirección se haría a la ruta '/' o '/home' ya que 'Login' fue borrada.
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ path: '/' }) 
  } else {
    next()
  }
})

// Actualiza el título de la página
router.afterEach((to) => {
  document.title = to.meta?.title || 'Sistema Académico'
})

export default router