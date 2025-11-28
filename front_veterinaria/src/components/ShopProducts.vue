<template>
  <section class="bg-white py-8 px-4 md:px-8 max-w-7xl mx-auto">
    <div class="flex flex-col lg:flex-row gap-8">
      
      <!-- Sidebar Filters -->
      <aside class="lg:w-72 flex-shrink-0">
        <div class="bg-gradient-to-br from-white to-gray-50 rounded-3xl shadow-xl p-6 sticky top-24 border border-gray-100">
          <!-- Header -->
          <div class="flex items-center justify-between mb-6 pb-4 border-b-2 border-gray-200">
            <h3 class="text-2xl font-serif font-bold text-gray-800 flex items-center gap-2">
              <svg class="w-6 h-6 text-[#1BB0B9]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              Filtros
            </h3>
          </div>
          
          <!-- Price Filter -->
          <div class="mb-6 pb-6 border-b border-gray-200">
            <h4 class="font-bold text-gray-800 mb-4 text-base flex items-center gap-2">
              <svg class="w-5 h-5 text-[#1BB0B9]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Precio
            </h4>
            <div class="space-y-3">
              <label class="flex items-center cursor-pointer group hover:bg-gray-100 p-2 rounded-lg transition-colors">
                <input type="checkbox" v-model="filters.price" value="0-50" class="mr-3 w-4 h-4 accent-[#1BB0B9] cursor-pointer">
                <span class="text-sm text-gray-700 font-medium group-hover:text-[#1BB0B9] transition-colors">S/. 0 - S/. 50</span>
              </label>
              <label class="flex items-center cursor-pointer group hover:bg-gray-100 p-2 rounded-lg transition-colors">
                <input type="checkbox" v-model="filters.price" value="50-100" class="mr-3 w-4 h-4 accent-[#1BB0B9] cursor-pointer">
                <span class="text-sm text-gray-700 font-medium group-hover:text-[#1BB0B9] transition-colors">S/. 50 - S/. 100</span>
              </label>
              <label class="flex items-center cursor-pointer group hover:bg-gray-100 p-2 rounded-lg transition-colors">
                <input type="checkbox" v-model="filters.price" value="100+" class="mr-3 w-4 h-4 accent-[#1BB0B9] cursor-pointer">
                <span class="text-sm text-gray-700 font-medium group-hover:text-[#1BB0B9] transition-colors">S/. 100+</span>
              </label>
            </div>
          </div>

          <!-- Category Filter -->
          <div class="mb-6 pb-6 border-b border-gray-200">
            <h4 class="font-bold text-gray-800 mb-4 text-base flex items-center gap-2">
              <svg class="w-5 h-5 text-[#1BB0B9]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              Categoría
            </h4>
            <div class="space-y-3">
              <label class="flex items-center cursor-pointer group hover:bg-gray-100 p-2 rounded-lg transition-colors">
                <input type="checkbox" v-model="filters.category" value="camas" class="mr-3 w-4 h-4 accent-[#1BB0B9] cursor-pointer">
                <span class="text-sm text-gray-700 font-medium group-hover:text-[#1BB0B9] transition-colors">Camas</span>
              </label>
              <label class="flex items-center cursor-pointer group hover:bg-gray-100 p-2 rounded-lg transition-colors">
                <input type="checkbox" v-model="filters.category" value="juguetes" class="mr-3 w-4 h-4 accent-[#1BB0B9] cursor-pointer">
                <span class="text-sm text-gray-700 font-medium group-hover:text-[#1BB0B9] transition-colors">Juguetes</span>
              </label>
              <label class="flex items-center cursor-pointer group hover:bg-gray-100 p-2 rounded-lg transition-colors">
                <input type="checkbox" v-model="filters.category" value="alimentos" class="mr-3 w-4 h-4 accent-[#1BB0B9] cursor-pointer">
                <span class="text-sm text-gray-700 font-medium group-hover:text-[#1BB0B9] transition-colors">Alimentos</span>
              </label>
            </div>
          </div>

          <!-- Color Filter -->
          <div class="mb-6 pb-6 border-b border-gray-200">
            <h4 class="font-bold text-gray-800 mb-4 text-base flex items-center gap-2">
              <svg class="w-5 h-5 text-[#1BB0B9]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
              Color
            </h4>
            <div class="flex flex-wrap gap-3">
              <button 
                v-for="color in colors" 
                :key="color.name"
                @click="toggleColor(color.name)"
                :class="filters.colors.includes(color.name) ? 'ring-2 ring-[#1BB0B9] ring-offset-2 scale-110' : 'hover:scale-105'"
                class="w-10 h-10 rounded-full border-2 border-gray-300 transition-all shadow-md hover:shadow-lg"
                :style="{ backgroundColor: color.hex }"
                :title="color.name"
              ></button>
            </div>
          </div>

          <!-- Size Filter -->
          <div class="mb-6 pb-6 border-b border-gray-200">
            <h4 class="font-bold text-gray-800 mb-4 text-base flex items-center gap-2">
              <svg class="w-5 h-5 text-[#1BB0B9]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
              </svg>
              Talla
            </h4>
            <div class="flex gap-2 flex-wrap">
              <button 
                v-for="size in sizes" 
                :key="size"
                @click="toggleSize(size)"
                :class="filters.sizes.includes(size) 
                  ? 'bg-gradient-to-br from-[#1BB0B9] to-[#16a0a8] text-white border-[#1BB0B9] shadow-lg scale-105' 
                  : 'bg-white text-gray-700 border-gray-300 hover:border-[#1BB0B9] hover:text-[#1BB0B9]'"
                class="px-5 py-2.5 rounded-xl border-2 text-sm font-bold transition-all"
              >
                {{ size }}
              </button>
            </div>
          </div>

          <!-- Brand Filter -->
          <div class="mb-6">
            <h4 class="font-bold text-gray-800 mb-4 text-base flex items-center gap-2">
              <svg class="w-5 h-5 text-[#1BB0B9]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
              </svg>
              Marca
            </h4>
            <div class="space-y-3">
              <label class="flex items-center cursor-pointer group hover:bg-gray-100 p-2 rounded-lg transition-colors">
                <input type="checkbox" v-model="filters.brands" value="PetComfort" class="mr-3 w-4 h-4 accent-[#1BB0B9] cursor-pointer">
                <span class="text-sm text-gray-700 font-medium group-hover:text-[#1BB0B9] transition-colors">PetComfort</span>
              </label>
              <label class="flex items-center cursor-pointer group hover:bg-gray-100 p-2 rounded-lg transition-colors">
                <input type="checkbox" v-model="filters.brands" value="CozyPaws" class="mr-3 w-4 h-4 accent-[#1BB0B9] cursor-pointer">
                <span class="text-sm text-gray-700 font-medium group-hover:text-[#1BB0B9] transition-colors">CozyPaws</span>
              </label>
              <label class="flex items-center cursor-pointer group hover:bg-gray-100 p-2 rounded-lg transition-colors">
                <input type="checkbox" v-model="filters.brands" value="DreamBed" class="mr-3 w-4 h-4 accent-[#1BB0B9] cursor-pointer">
                <span class="text-sm text-gray-700 font-medium group-hover:text-[#1BB0B9] transition-colors">DreamBed</span>
              </label>
            </div>
          </div>

          <!-- Clear Filters Button -->
          <button 
            @click="clearFilters"
            class="w-full py-3 px-4 bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 font-bold rounded-xl hover:from-red-50 hover:to-red-100 hover:text-red-600 transition-all duration-300 flex items-center justify-center gap-2 border border-gray-300 hover:border-red-300"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Limpiar filtros
          </button>
        </div>
      </aside>

      <!-- Main Content -->
      <main class="flex-1">
        <!-- Search Bar & Cart -->
        <div class="flex items-center gap-4 mb-8">
          <div class="flex-1 relative">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Buscar productos..." 
              class="w-full px-4 py-3 pl-12 rounded-xl border-2 border-gray-200 focus:border-[#1BB0B9] focus:outline-none transition-colors"
            >
            <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <button class="relative p-3 bg-[#1BB0B9] text-white rounded-xl hover:bg-[#16a0a8] transition-colors">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            <span class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full w-5 h-5 flex items-center justify-center">{{ cartCount }}</span>
          </button>
        </div>

        <!-- Products Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="product in filteredProducts" 
            :key="product.id"
            class="bg-white rounded-2xl overflow-hidden shadow-md hover:shadow-xl transition-all duration-300 group flex flex-col h-full"
          >
            <!-- Product Image -->
            <div class="relative h-56 overflow-hidden bg-gray-100 flex-shrink-0">
              <img 
                :src="product.image" 
                :alt="product.name" 
                class="w-full h-full object-contain p-4 transition-transform duration-500 group-hover:scale-110"
              />
              <div v-if="product.discount" class="absolute top-3 right-3 bg-red-500 text-white px-3 py-1 rounded-full text-xs font-bold">
                -{{ product.discount }}%
              </div>
            </div>

            <!-- Product Info -->
            <div class="p-5 flex flex-col flex-grow">
              <!-- Rating -->
              <div class="flex items-center gap-1 mb-2">
                <svg v-for="star in 5" :key="star" class="w-4 h-4" :class="star <= product.rating ? 'text-yellow-400' : 'text-gray-300'" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
                <span class="text-xs text-gray-500 ml-1">({{ product.reviews }})</span>
              </div>

              <!-- Name -->
              <h3 class="font-serif font-bold text-gray-800 mb-2 line-clamp-2">{{ product.name }}</h3>

              <!-- Price -->
              <div class="flex items-baseline gap-2 mb-4">
                <span class="text-2xl font-bold text-[#1BB0B9]">S/. {{ product.price.toFixed(2) }}</span>
                <span v-if="product.discount" class="text-sm text-gray-400 line-through">S/. {{ product.originalPrice.toFixed(2) }}</span>
              </div>

              <!-- Add to Cart Button -->
              <button 
                @click="addToCart(product)"
                class="w-full py-3 bg-[#1BB0B9] text-white font-bold rounded-xl hover:bg-[#16a0a8] transition-all duration-300 flex items-center justify-center gap-2 group-hover:shadow-lg mt-auto"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                <span>Agregar</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredProducts.length === 0" class="text-center py-20">
          <p class="text-gray-500 text-lg">No se encontraron productos con los filtros seleccionados.</p>
        </div>
      </main>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue';
import camaCircular from '@/assets/images/cama_circular.svg';
import camaLitera from '@/assets/images/cama_litera.svg';
import camaCesta from '@/assets/images/cama_cesta.svg';
import camaCuadrada from '@/assets/images/cama_cuadrada.svg';

const searchQuery = ref('');
const cartCount = ref(0);

const filters = ref({
  price: [],
  category: [],
  colors: [],
  sizes: [],
  brands: []
});

const colors = [
  { name: 'Beige', hex: '#F5F5DC' },
  { name: 'Gris', hex: '#808080' },
  { name: 'Azul', hex: '#4A90E2' },
  { name: 'Rosa', hex: '#FFB6C1' },
  { name: 'Verde', hex: '#90EE90' }
];

const sizes = ['S', 'M', 'L', 'XL'];

const products = [
  { id: 1, name: 'Cama Circular Premium', category: 'camas', price: 30.00, originalPrice: 35.29, discount: 15, rating: 5, reviews: 24, image: camaCircular, color: 'Beige', size: 'M', brand: 'PetComfort' },
  { id: 2, name: 'Cama Litera Doble', category: 'camas', price: 30.00, originalPrice: 35.29, discount: 15, rating: 4, reviews: 18, image: camaLitera, color: 'Gris', size: 'L', brand: 'CozyPaws' },
  { id: 3, name: 'Cama Cesta Acogedora', category: 'camas', price: 30.00, originalPrice: 35.29, discount: 15, rating: 5, reviews: 32, image: camaCesta, color: 'Beige', size: 'M', brand: 'DreamBed' },
  { id: 4, name: 'Cama Cuadrada Deluxe', category: 'camas', price: 30.00, originalPrice: 35.29, discount: 15, rating: 4, reviews: 15, image: camaCuadrada, color: 'Azul', size: 'L', brand: 'PetComfort' },
  { id: 5, name: 'Cama Circular Suave', category: 'camas', price: 30.00, originalPrice: 35.29, discount: 15, rating: 5, reviews: 28, image: camaCircular, color: 'Rosa', size: 'S', brand: 'CozyPaws' },
  { id: 6, name: 'Cama Cesta Confort', category: 'camas', price: 30.00, originalPrice: 35.29, discount: 15, rating: 4, reviews: 21, image: camaCesta, color: 'Verde', size: 'M', brand: 'DreamBed' }
];

const toggleColor = (color) => {
  const index = filters.value.colors.indexOf(color);
  if (index > -1) {
    filters.value.colors.splice(index, 1);
  } else {
    filters.value.colors.push(color);
  }
};

const toggleSize = (size) => {
  const index = filters.value.sizes.indexOf(size);
  if (index > -1) {
    filters.value.sizes.splice(index, 1);
  } else {
    filters.value.sizes.push(size);
  }
};

const clearFilters = () => {
  filters.value = {
    price: [],
    category: [],
    colors: [],
    sizes: [],
    brands: []
  };
  searchQuery.value = '';
};

const filteredProducts = computed(() => {
  let result = products;

  if (searchQuery.value) {
    result = result.filter(p => 
      p.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    );
  }

  if (filters.value.category.length > 0) {
    result = result.filter(p => filters.value.category.includes(p.category));
  }

  if (filters.value.colors.length > 0) {
    result = result.filter(p => filters.value.colors.includes(p.color));
  }

  if (filters.value.sizes.length > 0) {
    result = result.filter(p => filters.value.sizes.includes(p.size));
  }

  if (filters.value.brands.length > 0) {
    result = result.filter(p => filters.value.brands.includes(p.brand));
  }

  if (filters.value.price.length > 0) {
    result = result.filter(p => {
      return filters.value.price.some(range => {
        if (range === '0-50') return p.price >= 0 && p.price <= 50;
        if (range === '50-100') return p.price > 50 && p.price <= 100;
        if (range === '100+') return p.price > 100;
        return false;
      });
    });
  }

  return result;
});

const addToCart = (product) => {
  cartCount.value++;
  console.log('Added to cart:', product.name);
};
</script>
