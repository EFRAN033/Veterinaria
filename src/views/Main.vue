<template>
  <div class="main-container min-h-screen">
    <HeroSection />
    <Welcome /> </div>
</template>

<script setup>
import HeroSection from './HeroSection.vue';
import Welcome from './Welcome.vue'; // 1. Importar el nuevo componente
</script>

<style scoped>
.main-container {
  /* La clase Tailwind 'min-h-screen' ya hace esto, pero lo dejamos como comentario */
  /* min-height: 100vh; */
}
</style>