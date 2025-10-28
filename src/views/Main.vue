<template>
  <div class="main-container min-h-screen">
    <HeroSection />
    <Welcome /> </div>
    <Adoption />
</template>

<script setup>
import HeroSection from './HeroSection.vue';
import Welcome from './Welcome.vue'; // 
import Adoption from './Adoption.vue';
</script>

<style scoped>
.main-container {
  /* La clase Tailwind 'min-h-screen' ya hace esto, pero lo dejamos como comentario */
  /* min-height: 100vh; */
}
</style>