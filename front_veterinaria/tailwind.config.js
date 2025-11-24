/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      // Tus colores personalizados se mantienen intactos
      colors: {
        brand: {
          primary: '#d60579',
          light: '#fde9f2',
          medium: '#fbc7cc',
          dark: '#a6045d',
          accentPink: '#f79190',
        },
        accentBlue: '#73a4b3',
        success: '#22c55e',
        error: '#ef4444',
        warning: '#facc15',
        gray: {
          100: '#f7f7f7',
          200: '#ededed',
          300: '#e0e0e0',
          400: '#bdbdbd',
          500: '#9e9e9e',
          600: '#757575',
          700: '#424242',
          800: '#212121',
          900: '#1a1a1a',
        },
      },
      keyframes: {
        // --- TUS KEYFRAMES EXISTENTES ---
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'fade-in-down': {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'pop-in': {
          '0%': { transform: 'scale(0.9)', opacity: '0' },
          '80%': { transform: 'scale(1.05)', opacity: '1' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        pulse: {
          '0%, 100%': { transform: 'scale(1)' },
          '50%': { transform: 'scale(1.03)' },
        },
        'blob': {
          '0%': { transform: 'translate(0px, 0px) scale(1)' },
          '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
          '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
          '100%': { transform: 'translate(0px, 0px) scale(1)' },
        },
        
        // --- ✨ KEYFRAMES AÑADIDOS DE LA ÚLTIMA MEJORA ---
        'enter-from-bottom': {
          'from': { opacity: '0', transform: 'translateY(20px)' },
          'to': { opacity: '1', transform: 'translateY(0)' },
        },
        'gradient-anim': {
          '0%, 100%': { 'background-position': '0% 50%' },
          '50%': { 'background-position': '100% 50%' },
        },
        'shoot': {
            '0%': { transform: 'translate(-100%, 100%) rotate(45deg)' },
            '100%': { transform: 'translate(100%, -100%) rotate(45deg)' },
        },
        'wiggle': {
            '0%, 100%': { transform: 'rotate(-3deg)' },
            '50%': { transform: 'rotate(3deg)' },
        }
      },
      animation: {
        // --- TUS ANIMACIONES EXISTENTES ---
        'fade-in-up': 'fade-in-up 0.8s ease-out forwards',
        'fade-in-down': 'fade-in-down 0.8s ease-out forwards',
        'pop-in': 'pop-in 0.3s ease-out forwards',
        pulse: 'pulse 1.8s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'blob-slow': 'blob 10s infinite',

        // --- ✨ ANIMACIONES AÑADIDAS DE LA ÚLTIMA MEJORA ---
        'gradient-anim': 'gradient-anim 3s ease-in-out infinite',
        'shoot': 'shoot 8s ease-in-out infinite',
      },
    },
  },
  plugins: [],
}