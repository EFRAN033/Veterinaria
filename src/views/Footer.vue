<template>
    <footer class="site-footer">
      <div class="footer-container">
        <div class="footer-main">
          <div class="footer-column about-column">
            <h3 class="footer-title">VETERINARIA</h3>
            <p>
              Cuidando a tus mejores amigos con amor y profesionalismo. Ofrecemos servicios completos para garantizar la salud y felicidad de tus mascotas.
            </p>
          </div>
  
          <div class="footer-column links-column">
            <h3 class="footer-title">Enlaces Rápidos</h3>
            <ul>
              <li><a href="#">Inicio</a></li>
              <li><a href="#services">Servicios</a></li>
              <li><a href="#">Nosotros</a></li>
              <li><a href="#">Contacto</a></li>
            </ul>
          </div>
  
          <div class="footer-column contact-column">
            <h3 class="footer-title">Contacto</h3>
            <p>
              <span class="icon">📍</span> Av. Principal 123, Lima, Perú
            </p>
            <p>
              <span class="icon">📞</span> +51 987 654 321
            </p>
            <p>
              <span class="icon">✉️</span> contacto@veterinaria.com
            </p>
          </div>
        </div>
  
        <div class="footer-bottom">
          <p class="copyright-text">
            &copy; {{ currentYear }} Veterinaria. Todos los derechos reservados.
          </p>
          <div class="social-icons">
            <a href="#" aria-label="Facebook">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v2.385z"/></svg>
            </a>
            <a href="#" aria-label="Instagram">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.85s-.011 3.584-.069 4.85c-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07s-3.584-.012-4.85-.07c-3.252-.148-4.771-1.691-4.919-4.919-.058-1.265-.069-1.645-.069-4.85s.011-3.584.069-4.85c.149-3.225 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.85-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948s.014 3.667.072 4.947c.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072s3.667-.014 4.947-.072c4.358-.2 6.78-2.618 6.98-6.98.059-1.281.073-1.689.073-4.948s-.014-3.667-.072-4.947c-.2-4.358-2.618-6.78-6.98-6.98-1.281-.058-1.689-.072-4.948-.072zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.162 6.162 6.162 6.162-2.759 6.162-6.162-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4s1.791-4 4-4 4 1.79 4 4-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.441 1.441 1.441 1.441-.645 1.441-1.441-.645-1.44-1.441-1.44z"/></svg>
            </a>
            <a href="#" aria-label="Twitter">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616v.064c0 2.298 1.634 4.212 3.792 4.649-.65.177-1.344.226-2.061.077.608 1.88 2.368 3.247 4.452 3.284-1.785 1.395-4.033 2.226-6.489 2.226-.423 0-.84-.025-1.25-.074 2.308 1.482 5.063 2.344 8.041 2.344 9.648 0 14.931-7.996 14.636-14.646.99-.715 1.846-1.613 2.529-2.624z"/></svg>
            </a>
          </div>
        </div>
      </div>
    </footer>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  
  // Obtiene el año actual de forma dinámica para el copyright
  const currentYear = computed(() => new Date().getFullYear());
  </script>
  
  <style scoped>
  /* Estilos generales del footer */
  .site-footer {
    background-color: #26272b; /* Un gris oscuro casi negro */
    color: #a9a9a9; /* Un gris claro para el texto */
    padding: 45px 0 20px;
    font-size: 15px;
    line-height: 24px;
  }
  
  .footer-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
  }
  
  /* Estilos de la sección principal con columnas */
  .footer-main {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); /* Grilla responsiva */
    gap: 2rem; /* Espacio entre columnas */
    padding-bottom: 2rem;
    border-bottom: 1px solid #444; /* Línea separadora */
    margin-bottom: 2rem;
  }
  
  .footer-column {
    padding: 0 15px;
  }
  
  .footer-title {
    color: #ffffff; /* Títulos en blanco */
    font-size: 18px;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
  }
  
  /* Estilos específicos para cada columna */
  .about-column p {
    text-align: justify;
  }
  
  .links-column ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .links-column ul li a {
    color: #a9a9a9;
    text-decoration: none;
    display: block;
    padding: 5px 0;
    transition: color 0.3s ease;
  }
  
  .links-column ul li a:hover {
    color: #ffffff; /* Resaltar al pasar el cursor */
  }
  
  .contact-column p {
    display: flex;
    align-items: center;
    gap: 10px; /* Espacio entre el icono y el texto */
  }
  
  .contact-column .icon {
    font-size: 1.2rem;
  }
  
  /* Estilos de la barra inferior */
  .footer-bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap; /* Para que se apile en pantallas pequeñas */
    gap: 1rem;
  }
  
  .copyright-text {
    margin: 0;
    text-align: center;
    flex-grow: 1; /* Permite que ocupe el espacio sobrante */
  }
  
  /* Estilos de los iconos de redes sociales */
  .social-icons {
    display: flex;
    gap: 15px; /* Espacio entre iconos */
    flex-grow: 1;
    justify-content: center;
  }
  
  .social-icons a {
    color: #a9a9a9;
    font-size: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: color 0.3s ease, transform 0.3s ease;
  }
  
  .social-icons a:hover {
    color: #ffffff;
    transform: translateY(-3px); /* Efecto flotante */
  }
  
  /* Diseño responsivo para tablets y móviles */
  @media (min-width: 768px) {
    .copyright-text {
      text-align: left; /* Alinea a la izquierda en pantallas grandes */
    }
  
    .social-icons {
      justify-content: flex-end; /* Alinea a la derecha en pantallas grandes */
    }
  }
  </style>