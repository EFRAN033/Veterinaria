import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

// Función para decodificar el token JWT
function parseJwt(token) {
  try {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
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
  const isLoggedIn = ref(!!token.value)

  // --- GETTERS ---
  const userRole = computed(() => user.value?.role || null)
  const userName = computed(() => user.value?.name || '')
  const userShortName = computed(() => {
    if (!user.value?.name) return '';
    const parts = user.value.name.split(' ');
    if (parts.length >= 2) {
      // Return First Name + First Surname (assuming standard format)
      return `${parts[0]} ${parts[1]}`;
    }
    return user.value.name;
  })
  const userEmail = computed(() => user.value?.email || '')

  // --- ACTIONS ---
  function setUser(userData) {
    user.value = userData
    localStorage.setItem('user_info', JSON.stringify(userData))
    isLoggedIn.value = true
  }

  function setToken(newToken) {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('access_token', newToken)
      const userData = parseJwt(newToken)
      if (userData) {
        setUser(userData)
      }
    } else {
      clearUser()
    }
  }

  function clearUser() {
    token.value = null
    user.value = null
    isLoggedIn.value = false
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_info')
  }

  function logout() {
    clearUser()
  }

  return {
    token,
    user,
    isLoggedIn,
    userRole,
    userName,
    userShortName,
    userEmail,
    setUser,
    setToken,
    clearUser,
    logout
  }
})