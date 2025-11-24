<template>
  <div class="min-h-screen bg-white font-sans relative">
    <Header />
    <BackButton />
    
    <!-- Spacer removed to let image go under header --> 

    <main class="relative z-10 min-h-[60vh]">
      <!-- Header Image -->
      <div class="w-full h-64 md:h-96 overflow-hidden relative">
        <img 
          :src="publicidadImage" 
          alt="Pet Shop Header" 
          class="w-full h-full object-cover object-center"
        />

      </div>

      <!-- Shop Products Component -->
      <ShopProducts />
    </main>

    <Footer />
  </div>
</template>

<script setup>
import Header from './Header.vue';
import BackButton from '@/components/BackButton.vue';
import Footer from './Footer.vue';
import ShopProducts from '@/components/ShopProducts.vue';
import publicidadImage from '@/assets/images/Publicidad_1.png';
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

.font-sans { font-family: 'Montserrat', sans-serif; }
.font-serif { font-family: 'Playfair Display', serif; }
</style>
