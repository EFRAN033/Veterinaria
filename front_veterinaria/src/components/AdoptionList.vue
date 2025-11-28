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
          
          <button @click="openAdoptionModal(pet)" class="w-full py-3 rounded-xl border-2 border-[#BEDC74] text-[#1a5f63] font-bold hover:bg-[#BEDC74] hover:text-white transition-colors duration-300 flex items-center justify-center gap-2">
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
    <!-- Adoption Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showModal = false"></div>
      <div class="bg-white rounded-3xl shadow-2xl w-full max-w-md relative z-10 overflow-hidden animate-fade-in-up">
        <div class="bg-[#1BB0B9] p-6 text-white text-center relative">
          <button @click="showModal = false" class="absolute top-4 right-4 text-white/80 hover:text-white">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          <h3 class="text-2xl font-serif font-bold mb-1">¡Gracias por tu interés!</h3>
          <p class="text-[#BFF1F6] text-sm">Estás a un paso de cambiar una vida.</p>
        </div>
        <div class="p-8 text-center">
          <div class="w-20 h-20 bg-[#BEDC74]/20 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-[#1a5f63]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
            </svg>
          </div>
          <p class="text-gray-600 mb-6">
            Para iniciar el proceso de adopción de <span class="font-bold text-[#1BB0B9]">{{ selectedPet?.name }}</span>, por favor contáctanos o visítanos.
          </p>
          <div class="space-y-3">
            <a :href="`tel:${selectedPet?.phone}`" class="block w-full py-3 rounded-xl bg-[#BEDC74] text-[#1a5f63] font-bold hover:bg-[#d4ed95] transition-colors">
              Llamar ahora
            </a>
            <button @click="showModal = false" class="block w-full py-3 rounded-xl border-2 border-gray-100 text-gray-500 font-bold hover:bg-gray-50 transition-colors">
              Seguir mirando
            </button>
          </div>
        </div>
      </div>
    </div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import apiClient from '@/axios';

const categories = ['Todos', 'Perros', 'Gatos', 'Aves', 'Hámsters', 'Peces', 'Otro'];
const selectedCategory = ref('Todos');
const showModal = ref(false);
const selectedPet = ref(null);
const pets = ref([]);
const loading = ref(true);
const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

const openAdoptionModal = (pet) => {
  selectedPet.value = pet;
  showModal.value = true;
};

const fetchAdoptions = async () => {
  try {
    const response = await apiClient.get('/v1/adoptions/');
    pets.value = response.data.map(pet => ({
      id: pet.id,
      name: pet.name,
      category: pet.species + 's', // Simple pluralization for matching categories
      species: pet.species,
      breed: pet.breed || 'Mestizo',
      age: pet.age,
      gender: pet.gender,
      image: pet.images && pet.images.length > 0 ? `${backendUrl}${pet.images[0]}` : 'https://placehold.co/500x500?text=No+Image',
      description: pet.description || 'Sin descripción',
      phone: pet.phone
    }));
  } catch (error) {
    console.error("Error fetching adoptions:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchAdoptions();
});

const filteredPets = computed(() => {
  if (selectedCategory.value === 'Todos') return pets.value;
  // Normalize category matching
  const cat = selectedCategory.value.slice(0, -1); // Remove 's' roughly
  return pets.value.filter(pet => {
    if (selectedCategory.value === 'Perros') return pet.species === 'Perro';
    if (selectedCategory.value === 'Gatos') return pet.species === 'Gato';
    if (selectedCategory.value === 'Aves') return pet.species === 'Aves';
    if (selectedCategory.value === 'Hámsters') return pet.species === 'Hámster';
    if (selectedCategory.value === 'Peces') return pet.species === 'Peces';
    return pet.species === selectedCategory.value;
  });
});
</script>
