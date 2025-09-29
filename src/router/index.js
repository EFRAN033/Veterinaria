// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
// Asegúrate de que este archivo exista si vas a usar useUserStore
import { useUserStore } from '@/stores/user' 

// --- Vistas a Mantener ---
// Main.vue es el layout principal.
const Main = () => import('../views/Main.vue') 
// HeroSection.vue está aquí, aunque ya lo estás importando en Main.vue
// Lo incluimos si quisieras usarlo directamente en una ruta en el futuro.
const HeroSection = () => import('../views/HeroSection.vue') 


const routes = [
  // Redirección por defecto
  { path: '/', redirect: '/home' }, 
  
  // Ruta principal
  {
    path: '/home',
    name: 'Home',
    component: Main, // Main.vue es el componente padre
    meta: { title: 'Página Principal' },
    children: [
      {
        path: 'hero', // Ruta anidada: /home/hero
        name: 'Hero',
        component: HeroSection, // HeroSection.vue es un componente hijo
        meta: { title: 'Sección Hero' }
      }
    ]
  },

  // Ruta para páginas no encontradas (404)
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    // Componente inline simple para el 404
    component: { template: `<div class="p-8"><h1 class="font-bold text-2xl">404 - No Encontrado</h1><router-link to="/home" class="text-indigo-600">Volver al inicio</router-link></div>` },
    meta: { title: '404 | No Encontrado' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  // Asegura que la página se desplace al principio en cada navegación
  scrollBehavior: () => ({ top: 0 }) 
})

// Guardián de navegación
router.beforeEach((to, from, next) => {
  const userStore = useUserStore() 
  
  // Lógica para rutas que requieren autenticación.
  // Como 'Login' fue borrado, si falla la auth, redirige a la ruta '/' (que redirige a '/home').
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next({ path: '/' }) 
  } else {
    next()
  }
})

// Actualiza el título de la pestaña del navegador después de la navegación
router.afterEach((to) => {
  document.title = to.meta?.title || 'Sistema Académico'
})

export default router