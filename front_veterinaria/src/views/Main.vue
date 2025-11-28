<template>
  <main class="min-h-screen">
    <HeroSection />
    <Welcome />
    <Adoption />

    <div class="w-full">
      <img :src="divisionImage" alt="Divisor de sección" class="w-full h-60 object-cover" loading="lazy" />
    </div>

    <Shop />
    <Services />
    <carousel />
    <Footer />
  </main>
</template>

<script setup>
import HeroSection from './HeroSection.vue';
import Welcome from './Welcome.vue'; 
import divisionImage from '@/assets/images/Division.png';
import { defineAsyncComponent } from 'vue';

const Adoption = defineAsyncComponent(() => import('./Adoption.vue'));
const Shop = defineAsyncComponent(() => import('./Shop.vue'));
const Services = defineAsyncComponent(() => import('./Services.vue'));
const carousel = defineAsyncComponent(() => import('./carousel.vue'));
const Footer = defineAsyncComponent(() => import('./Footer.vue'));
</script>

<style scoped>

</style>