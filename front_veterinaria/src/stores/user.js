import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

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
  const token = ref(localStorage.getItem('access_token') || null)
  const user = ref(JSON.parse(localStorage.getItem('user_info')) || null)
  const isLoggedIn = computed(() => !!token.value)

  const userRole = computed(() => user.value?.role || null)
  const userName = computed(() => user.value?.name || '')
  const userShortName = computed(() => {
    if (!user.value?.name) return '';
    const parts = user.value.name.split(' ');
    if (parts.length >= 2) {
      return `${parts[0]} ${parts[1]}`;
    }
    return user.value.name;
  })
  const userEmail = computed(() => user.value?.email || '')

  function setUser(userData) {
    user.value = userData
    localStorage.setItem('user_info', JSON.stringify(userData))
  }

  function setToken(newToken) {
    console.log('userStore: setToken called', newToken ? 'with token' : 'null');
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
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_info')
  }

  function logout() {
    clearUser()
  }

  async function fetchProfile() {
    try {
      const { default: axios } = await import('../axios');
      const response = await axios.get('/v1/auth/me');
      setUser(response.data);
      return response.data;
    } catch (error) {
      console.error('Error fetching profile:', error);
      throw error;
    }
  }

  async function fetchAppointments() {
    try {
      const { default: axios } = await import('../axios');
      const response = await axios.get('/v1/appointments/');
      return response.data;
    } catch (error) {
      console.error('Error fetching appointments:', error);
      throw error;
    }
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
    logout,
    fetchProfile,
    fetchAppointments
  }
})