<template>
  <section id="shop" class="w-full py-24 px-4 md:px-16 bg-gray-50 font-sans relative overflow-hidden">
    
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
      <div class="absolute top-[-10%] right-[-5%] w-96 h-96 bg-[#02939E]/5 rounded-full blur-3xl"></div>
      <div class="absolute bottom-[-10%] left-[-5%] w-96 h-96 bg-[#a4ad74]/5 rounded-full blur-3xl"></div>
    </div>

    <div class="max-w-7xl mx-auto relative z-10">

      <div class="text-center mb-12">
        <span class="text-[#a4ad74] font-bold tracking-[0.2em] uppercase text-xs md:text-sm mb-3 block">
          Mima a tu mascota
        </span>
        <h2 class="text-4xl md:text-5xl font-serif font-bold text-gray-900 tracking-tight mb-6">
          Pet <span class="text-[#02939E]">Shop</span>
        </h2>
        <div class="w-16 h-1 bg-[#02939E] mx-auto rounded-full"></div>
      </div>

      <div class="flex flex-wrap justify-center gap-3 mb-12">
        <button 
          v-for="cat in categories" 
          :key="cat"
          @click="activeCategory = cat"
          :class="[
            'px-6 py-2.5 rounded-full text-sm font-bold tracking-wide transition-all duration-300 border',
            activeCategory === cat 
              ? 'bg-[#02939E] text-white border-[#02939E] shadow-lg shadow-[#02939E]/20 transform -translate-y-1' 
              : 'bg-white text-gray-600 border-gray-200 hover:border-[#02939E] hover:text-[#02939E]'
          ]"
        >
          {{ cat }}
        </button>
        <a href="#" class="flex items-center px-6 py-2.5 text-sm font-bold text-[#a4ad74] hover:underline underline-offset-4 uppercase tracking-widest ml-4">
          Ver Todo →
        </a>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
        
        <div 
          v-for="(product, index) in products" 
          :key="index" 
          class="group bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-500 ease-out overflow-hidden border border-gray-100 flex flex-col"
        >
          <div class="relative h-64 w-full bg-gray-100 overflow-hidden flex items-center justify-center p-4">
            <span v-if="product.discount" class="absolute top-3 left-3 bg-[#a4ad74] text-white text-[10px] font-bold px-2 py-1 rounded-md shadow-sm z-10">
              -{{ product.discount }}
            </span>
            
            <button class="absolute top-3 right-3 p-2 rounded-full bg-white/80 text-gray-400 hover:text-red-500 hover:bg-white transition-colors z-10 shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
                <path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.691 2.25 5.353 4.814 3.25 7.875 3.25c1.227 0 2.363.436 3.248 1.217.885-.781 2.02-1.217 3.247-1.217 3.061 0 5.625 2.103 5.625 5.441 0 3.483-2.438 6.67-4.743 8.817a25.18 25.18 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z" />
              </svg>
            </button>

            <img 
              :src="product.image" 
              :alt="product.name" 
              class="h-full w-full object-contain transition-transform duration-500 group-hover:scale-110"
            >
          </div>

          <div class="p-6 flex flex-col flex-grow">
            <div class="flex text-yellow-400 text-xs mb-2">
              <span v-for="n in 5" :key="n">
                <span v-if="n <= product.rating">★</span>
                <span v-else class="text-gray-300">★</span>
              </span>
              <span class="text-gray-400 ml-1 text-[10px]">({{ product.reviews }})</span>
            </div>

            <h3 class="text-lg font-bold text-gray-800 mb-1 group-hover:text-[#02939E] transition-colors">
              {{ product.name }}
            </h3>
            
            <div class="flex items-end gap-2 mb-4">
              <span class="text-xl font-bold text-[#02939E]">S/. {{ product.price }}</span>
              <span v-if="product.oldPrice" class="text-sm text-gray-400 line-through mb-1">S/. {{ product.oldPrice }}</span>
            </div>

            <button class="mt-auto w-full bg-gray-900 text-white py-3 rounded-lg font-bold text-sm uppercase tracking-wider hover:bg-[#02939E] transition-colors duration-300 shadow-md hover:shadow-lg flex items-center justify-center gap-2 group-hover:translate-y-0">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007z" />
              </svg>
              Agregar
            </button>
          </div>
        </div>

      </div>

    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import camaCircularImage from '@/assets/images/cama_circular.svg';
import camaCestaImage from '@/assets/images/cama_cesta.svg';
import camaCuadradaImage from '@/assets/images/cama_cuadrada.svg';
import camaLiteraImage from '@/assets/images/cama_litera.svg';

const activeCategory = ref('Camas');
const categories = ['Camas', 'Alimento', 'Juguetes', 'Ropa', 'Accesorios'];

const products = [
  { 
    name: 'Cama Circular Premium', 
    price: '30.00', 
    oldPrice: '45.00',
    discount: '33%', 
    rating: 5, 
    reviews: 128,
    image: camaCircularImage 
  },
  { 
    name: 'Cama Cesta Tejida', 
    price: '30.00', 
    oldPrice: null,
    discount: null, 
    rating: 4, 
    reviews: 85,
    image: camaCestaImage 
  },
  { 
    name: 'Cama Cuadrada Soft', 
    price: '30.00', 
    oldPrice: '35.00',
    discount: '15%', 
    rating: 5, 
    reviews: 42,
    image: camaCuadradaImage 
  },
  { 
    name: 'Litera para Gatos', 
    price: '30.00', 
    oldPrice: null,
    discount: null, 
    rating: 4, 
    reviews: 67,
    image: camaLiteraImage 
  },
];
</script>