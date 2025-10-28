<template>
    <section id="services" class="services-section">
      <div class="container">
        <h2 class="section-title">SERVICIOS</h2>
  
        <div class="services-grid">
          <div v-for="service in services" :key="service.id" class="service-card">
            <div class="card-image-wrapper">
              <img :src="service.image" :alt="service.title" class="service-image-svg" />
            </div>
            <div class="service-name-overlay">
              <h3 class="service-title-overlay">{{ service.title }}</h3>
            </div>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  // Importamos tus archivos SVG
  import agendarCitaSvg from '@/assets/images/agendar_cita.svg';
  import vacunacionSvg from '@/assets/images/vacunacion.svg';
  import nutricionSvg from '@/assets/images/nutricion.svg';
  import limpiezaDentalSvg from '@/assets/images/limpieza_dental.svg';
  import banoSvg from '@/assets/images/bano.svg';
  import corteSvg from '@/assets/images/corte.svg';
  
  const services = ref([
    {
      id: 1,
      title: 'Agendar Cita',
      image: agendarCitaSvg,
    },
    {
      id: 2,
      title: 'Vacunación',
      image: vacunacionSvg,
    },
    {
      id: 3,
      title: 'Nutrición',
      image: nutricionSvg,
    },
    {
      id: 4,
      title: 'Limpieza dental',
      image: limpiezaDentalSvg,
    },
    {
      id: 5,
      title: 'Baño',
      image: banoSvg,
    },
    {
      id: 6,
      title: 'Corte',
      image: corteSvg,
    },
  ]);
  </script>
  
  <style scoped>
  /* ... (los estilos de services-section, container, section-title y services-grid no cambian) ... */
  .services-section {
    padding: 2rem 1rem;
    background-color: #ffffff;
    text-align: center;
  }
  
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .section-title {
    font-size: 2.5rem;
    font-weight: 300;
    letter-spacing: 0.2em;
    margin-bottom: 4rem;
    color: #333333;
    text-transform: uppercase;
  }
  
  .services-grid {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    gap: 2rem;
    justify-items: center;
  }
  
  @media (min-width: 640px) {
    .services-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }
  
  @media (min-width: 1024px) {
    .services-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
  
  /* Tarjeta de servicio individual */
  .service-card {
    position: relative;
    width: 100%;
    max-width: 300px;
    height: 250px;
    overflow: hidden;
    border-radius: 1rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
    background-color: #f8f9fa; /* Este color se verá si el SVG tiene transparencias */
  }
  
  .service-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }
  
  /* --- CAMBIO AQUÍ --- */
  .card-image-wrapper {
    /* Define el área superior de la tarjeta */
    width: 100%;
    height: 100%; /* La imagen ocupará toda la tarjeta por defecto */
    position: relative; /* Para que la imagen se posicione dentro */
    overflow: hidden; /* Asegura que la imagen no se salga de los bordes */
  }
  
  /* --- CAMBIO AQUÍ --- */
  .service-image-svg {
    width: 100%; /* Ocupa el 100% del ancho del wrapper */
    height: 100%; /* Ocupa el 100% de la altura del wrapper */
    object-fit: cover; /* ESTA ES LA CLAVE: Escala la imagen para cubrir el contenedor. Puede recortar partes. */
    display: block;
  }
  
  /* Capa superpuesta con el nombre del servicio */
  .service-name-overlay {
    position: absolute; /* Se superpone sobre el card-image-wrapper */
    bottom: 0;
    left: 0;
    width: 100%;
    height: 35%;
    background-image: url('@/assets/images/senalservicio.png');
    background-size: cover;
    background-position: center bottom;
    background-repeat: no-repeat;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem 1rem;
    color: #333333;
    font-weight: 600;
    font-size: 1.1rem;
    text-align: center;
    box-sizing: border-box;
  }
  
  .service-title-overlay {
    margin: 0;
  }
  </style>