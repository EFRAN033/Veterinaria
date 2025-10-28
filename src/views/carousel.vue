<template>
    <section id="auto-carousel" class="carousel-section">
      <div 
        class="carousel-wrapper"
        @mouseenter="stopAutoScroll"
        @mouseleave="startAutoScroll"
      >
        <button @click="scrollLeft" class="carousel-button prev-button" aria-label="Anterior">
          &#10094;
        </button>
  
        <div class="carousel-track" ref="carouselTrack">
          <div v-for="item in carouselItems" :key="item.id" class="carousel-card">
            <p>{{ item.text }}</p>
          </div>
        </div>
  
        <button @click="scrollRight" class="carousel-button next-button" aria-label="Siguiente">
          &#10095;
        </button>
      </div>
    </section>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue';
  
  // Referencia al elemento del carrusel para manipular el scroll
  const carouselTrack = ref(null);
  // Variable para guardar el ID del intervalo y poder limpiarlo después
  const intervalId = ref(null);
  
  // Datos de ejemplo para las tarjetas del carrusel
  const carouselItems = ref([
    { id: 1, text: 'Producto 1' },
    { id: 2, text: 'Producto 2' },
    { id: 3, text: 'Producto 3' },
    { id: 4, text: 'Producto 4' },
    { id: 5, text: 'Producto 5' },
    { id: 6, text: 'Producto 6' },
    { id: 7, text: 'Producto 7' },
    { id: 8, text: 'Producto 8' },
  ]);
  
  // --- LÓGICA DEL CARRUSEL AUTOMÁTICO ---
  
  const scrollAmount = 300; // Cantidad de píxeles a desplazar
  
  const scrollRight = () => {
    const track = carouselTrack.value;
    if (!track) return;
  
    // Comprueba si ha llegado al final del scroll
    if (track.scrollLeft + track.clientWidth + 1 >= track.scrollWidth) {
      // Si está al final, vuelve al principio suavemente
      track.scrollTo({
        left: 0,
        behavior: 'smooth'
      });
    } else {
      // Si no, sigue desplazándose a la derecha
      track.scrollBy({
        left: scrollAmount,
        behavior: 'smooth'
      });
    }
  };
  
  const scrollLeft = () => {
    if (carouselTrack.value) {
      carouselTrack.value.scrollBy({
        left: -scrollAmount,
        behavior: 'smooth'
      });
    }
  };
  
  // Función para iniciar el desplazamiento automático
  const startAutoScroll = () => {
    if (intervalId.value) return;
    intervalId.value = setInterval(() => {
      scrollRight();
    }, 3000); // Cambia de tarjeta cada 3 segundos
  };
  
  // Función para detener el desplazamiento automático
  const stopAutoScroll = () => {
    clearInterval(intervalId.value);
    intervalId.value = null;
  };
  
  // --- CICLO DE VIDA DEL COMPONENTE ---
  
  onMounted(() => {
    startAutoScroll();
  });
  
  onUnmounted(() => {
    stopAutoScroll();
  });
  
  </script>
  
  <style scoped>
  .carousel-section {
    padding: 2rem 1rem; /* Reduje el padding superior ya que no hay título */
    background-color: #f8f9fa;
    /* El max-width y margin auto aseguran que el carrusel no sea demasiado ancho en pantallas grandes */
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .carousel-wrapper {
    position: relative;
    display: flex;
    align-items: center;
  }
  
  .carousel-track {
    display: flex;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    padding: 1rem 0;
    gap: 1.5rem;
    border-radius: 1rem;
  }
  
  .carousel-track::-webkit-scrollbar {
    display: none;
  }
  .carousel-track {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }
  
  .carousel-card {
    flex: 0 0 auto;
    width: 250px;
    height: 150px;
    background-color: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 0.5rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.1rem;
    color: #555;
    scroll-snap-align: start;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .carousel-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  }
  
  .carousel-button {
    background-color: white;
    color: #333;
    border: 1px solid #ddd;
    padding: 0.8rem 1.2rem;
    border-radius: 50%;
    cursor: pointer;
    font-size: 1.5rem;
    line-height: 1;
    position: absolute;
    z-index: 10;
    transform: translateY(-50%);
    top: 50%;
    transition: background-color 0.3s ease, box-shadow 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  }
  
  .carousel-button:hover {
    background-color: #f1f1f1;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
  }
  
  .prev-button {
    left: -25px;
  }
  
  .next-button {
    right: -25px;
  }
  
  @media (max-width: 768px) {
    .carousel-button {
      display: none;
    }
  }
  </style>