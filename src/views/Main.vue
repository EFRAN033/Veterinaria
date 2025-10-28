<template>
  <main class="min-h-screen">
    <HeroSection />
    <Welcome />
    <Adoption />

    <div class="w-full">
      <img :src="divisionImage" alt="Divisor de sección" class="w-full h-60 object-cover" />
    </div>

    <Shop />
    <Services />

  </main>
</template>

<script setup>
import HeroSection from './HeroSection.vue';
import Welcome from './Welcome.vue'; 
import Adoption from './Adoption.vue';
import divisionImage from '@/assets/images/Division.png';
// NUEVO: Importa el componente Shop
import Shop from './Shop.vue'; 
import Services from './Services.vue';
</script>

<style scoped>
/* Estilos específicos si los necesitas */
</style>