<template>
  <button 
    v-if="!isHomePage"
    @click="goBack" 
    class="fixed left-0 top-24 z-50 bg-[#00959E] hover:bg-[#007f87] text-white w-24 h-14 flex items-center justify-center rounded-r-[10px] shadow-lg transition-all duration-300 group hover:w-28 overflow-hidden"
    aria-label="Volver"
  >
    <img 
      src="@/assets/images/catpatas.png" 
      alt="Volver"
      class="w-12 h-12 object-contain transform rotate-[-112deg] scale-[1.3] group-hover:-translate-x-1 transition-transform duration-300"
    />
  </button>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import { computed } from 'vue';

const router = useRouter();
const route = useRoute();

const isHomePage = computed(() => {
  return route.path === '/' || route.path === '/home';
});

const goBack = () => {
  router.push('/');
};
</script>

<style scoped>
button {
  box-shadow: 2px 4px 10px rgba(0, 0, 0, 0.15);
}
</style>