import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Función para decodificar el token JWT (esta se mantiene igual)
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    return JSON.parse(jsonPayload);
  } catch (e) {
    console.error('Error decodificando el token:', e);
    return null;
  }
}


export const useUserStore = defineStore('user', () => {
  // --- STATE ---
  const token = ref(localStorage.getItem('access_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user_info')) || null)
  
  // --- ✨ CORRECCIÓN AQUÍ ---
  // isLoggedIn ahora es un 'ref' para poder modificarlo
  const isLoggedIn = ref(!!token.value) 

  // --- GETTERS ---
  // userRole se mantiene como computed, lo cual es correcto
  const userRole = computed(() => user.value?.role || null)

  // --- ACTIONS ---
  function setToken(newToken) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('access_token', newToken)
      const userData = parseJwt(newToken)
      user.value = userData
      localStorage.setItem('user_info', JSON.stringify(userData))
      
      isLoggedIn.value = true // Ahora esto funciona
    } else {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_info')
      user.value = null
      isLoggedIn.value = false // Y esto también
    }
  }

  function logout() {
    setToken(null)
  }

  return { token, user, isLoggedIn, userRole, setToken, logout }
})