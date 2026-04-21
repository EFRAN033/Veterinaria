/**
 * Si la app se sirve por HTTPS y la URL del env sigue en http://, el navegador
 * bloquea la petición ("Mixed Content"). Se fuerza https:// en el cliente.
 * Lo ideal sigue siendo definir VITE_API_URL con https en el despliegue.
 */
function upgradeHttpToHttpsWhenPageIsSecure(url) {
  if (typeof url !== 'string' || !url) return url;
  if (typeof window === 'undefined' || window.location.protocol !== 'https:') return url;
  if (url.startsWith('http://')) return `https://${url.slice('http://'.length)}`;
  return url;
}

/** Base del API (misma ruta que usa `apiClient` en axios). */
export function getApiBaseUrl() {
  const raw = import.meta.env.VITE_API_URL || '/api';
  if (typeof raw === 'string' && raw.startsWith('/')) return raw;
  return upgradeHttpToHttpsWhenPageIsSecure(raw);
}

/** Origen para assets/imagenes servidos por el backend (si aplica). */
export function getBackendBaseUrl() {
  const raw = import.meta.env.VITE_BACKEND_URL || '';
  return upgradeHttpToHttpsWhenPageIsSecure(raw);
}
