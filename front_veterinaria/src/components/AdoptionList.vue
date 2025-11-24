<template>
  <section class="bg-white py-16 px-4 md:px-8 max-w-7xl mx-auto">
    
    <div class="text-center mb-12">
      <h2 class="text-3xl md:text-4xl font-serif font-bold text-gray-800 mb-4">
        Encuentra a tu <span class="text-[#1BB0B9]">compañero ideal</span>
      </h2>
      <p class="text-gray-600 max-w-2xl mx-auto">
        Explora nuestras categorías y conoce a los pequeños que esperan por un hogar.
      </p>
    </div>

    <!-- Filters -->
    <div class="flex flex-wrap justify-center gap-4 mb-12">
      <button 
        v-for="category in categories" 
        :key="category"
        @click="selectedCategory = category"
        class="px-6 py-2 rounded-full text-sm font-bold tracking-wide transition-all duration-300 border-2"
        :class="selectedCategory === category 
          ? 'bg-[#1BB0B9] text-white border-[#1BB0B9] shadow-lg scale-105' 
          : 'bg-white text-gray-500 border-gray-200 hover:border-[#BEDC74] hover:text-[#1a5f63]'"
      >
        {{ category }}
      </button>
    </div>

    <!-- Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
      <div 
        v-for="pet in filteredPets" 
        :key="pet.id"
        class="bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 group hover:-translate-y-2 border border-gray-100"
      >
        <!-- Image Container -->
        <div class="relative h-64 overflow-hidden">
          <img 
            :src="pet.image" 
            :alt="pet.name" 
            class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
          />
          <div class="absolute top-4 right-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-bold text-[#1a5f63] shadow-sm">
            {{ pet.age }}
          </div>
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
        </div>

        <!-- Content -->
        <div class="p-6">
          <div class="flex justify-between items-start mb-2">
            <h3 class="text-xl font-serif font-bold text-gray-800">{{ pet.name }}</h3>
            <span class="text-2xl" :title="pet.gender === 'Macho' ? 'Macho' : 'Hembra'">
              {{ pet.gender === 'Macho' ? '♂' : '♀' }}
            </span>
          </div>
          
          <p class="text-[#1BB0B9] text-sm font-medium mb-2">{{ pet.breed }}</p>
          <p class="text-gray-500 text-sm mb-4 line-clamp-2">{{ pet.description }}</p>
          
          <button class="w-full py-3 rounded-xl border-2 border-[#BEDC74] text-[#1a5f63] font-bold hover:bg-[#BEDC74] hover:text-white transition-colors duration-300 flex items-center justify-center gap-2">
            <span>Adoptar</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredPets.length === 0" class="text-center py-20">
      <p class="text-gray-500 text-lg">No hay mascotas disponibles en esta categoría por el momento.</p>
    </div>

  </section>
</template>

<script setup>
import { ref, computed } from 'vue';

// Mock Data Images (using placeholders or imported assets if available, for now using placeholders/urls)
// In a real app, these would be dynamic. Using generic placeholders for demo.
const getPlaceholder = (type) => `https://source.unsplash.com/400x400/?${type}`;

const categories = ['Todos', 'Perros', 'Gatos', 'Aves', 'Hámsters', 'Peces'];
const selectedCategory = ref('Todos');

const pets = [
  { id: 1, name: 'Max', category: 'Perros', breed: 'Golden Retriever', age: '2 años', gender: 'Macho', image: 'https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=400&q=80', description: 'Max es un perro muy juguetón y cariñoso, le encanta correr por el parque.' },
  { id: 2, name: 'Luna', category: 'Gatos', breed: 'Siamés', age: '1 año', gender: 'Hembra', image: 'https://images.unsplash.com/photo-1513245543132-31f507417b26?auto=format&fit=crop&w=400&q=80', description: 'Luna es tranquila y elegante, ideal para un hogar relajado.' },
  { id: 3, name: 'Rocky', category: 'Perros', breed: 'Bulldog Francés', age: '3 años', gender: 'Macho', image: 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&w=400&q=80', description: 'Rocky es un compañero leal y protector, perfecto para familias.' },
  { id: 4, name: 'Coco', category: 'Aves', breed: 'Periquito', age: '6 meses', gender: 'Macho', image: 'https://images.unsplash.com/photo-1552728089-57bdde30beb8?auto=format&fit=crop&w=400&q=80', description: 'Coco es muy alegre y le gusta cantar por las mañanas.' },
  { id: 5, name: 'Molly', category: 'Hámsters', breed: 'Sirio', age: '5 meses', gender: 'Hembra', image: 'https://images.unsplash.com/photo-1425082661705-1834bfd09dca?auto=format&fit=crop&w=400&q=80', description: 'Molly es curiosa y activa, le encanta su rueda de ejercicios.' },
  { id: 6, name: 'Nemo', category: 'Peces', breed: 'Payaso', age: '1 año', gender: 'Macho', image: 'https://images.unsplash.com/photo-1524704654690-b56c05c78a00?auto=format&fit=crop&w=400&q=80', description: 'Nemo es colorido y vivaz, una joya para cualquier acuario.' },
  { id: 7, name: 'Simba', category: 'Gatos', breed: 'Persa', age: '4 años', gender: 'Macho', image: 'https://images.unsplash.com/photo-1574158622682-e40e69881006?auto=format&fit=crop&w=400&q=80', description: 'Simba es majestuoso y le encantan las caricias suaves.' },
  { id: 8, name: 'Bella', category: 'Perros', breed: 'Labrador', age: '1.5 años', gender: 'Hembra', image: 'https://images.unsplash.com/photo-1591769225440-811ad7d6eca6?auto=format&fit=crop&w=400&q=80', description: 'Bella es inteligente y aprende trucos muy rápido.' },
];

const filteredPets = computed(() => {
  if (selectedCategory.value === 'Todos') return pets;
  return pets.filter(pet => pet.category === selectedCategory.value);
});
</script>
