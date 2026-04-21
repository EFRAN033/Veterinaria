// Credenciales de demostración del panel Staff (sin backend ni base de datos).
// Cambia aquí si enlazas más adelante a una API real.
window.SISTEMA_DEMO_LOGIN = {
    usuario: 'demo',
    password: 'demo'
};

// Configuración de Tailwind y constantes del sistema
window.tailwind = window.tailwind || {};
window.tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: '#02939E',
                secondary: '#CDE262',
                neutral: '#848484',
            }
        }
    }
};