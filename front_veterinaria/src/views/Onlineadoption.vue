<template>
  <div class="min-h-screen bg-white font-sans overflow-x-hidden relative selection:bg-[#BEDC74] selection:text-[#1a5f63]">
    <Header />
    <BackButton />
    
    <div class="h-20 lg:h-28"></div> 

    <main class="container mx-auto px-4 pb-16 relative z-10">
      
      <div class="flex flex-col lg:flex-row items-center justify-center gap-10 lg:gap-16 max-w-7xl mx-auto">
        
        <div class="w-full lg:w-5/12 flex flex-col items-center lg:items-start relative z-20 text-center lg:text-left">
          
          <div class="relative group mb-8 transition-transform duration-500 hover:-translate-y-2">
            <div class="absolute inset-0 bg-[#BEDC74]/40 rounded-full blur-3xl transform translate-y-4 pointer-events-none opacity-70"></div>
            <img
              :src="doghuella"
              alt="Mascota"
              class="relative w-72 md:w-96 object-contain z-10 drop-shadow-2xl"
            />
          </div>

          <h1 class="font-serif text-4xl lg:text-5xl text-gray-800 font-bold mb-4 leading-tight">
            Dale una <br>
            <span class="text-[#1BB0B9]">segunda oportunidad.</span>
          </h1>
          <p class="text-gray-600 text-lg mb-8 max-w-md mx-auto lg:mx-0 leading-relaxed">
            El proceso es simple, seguro y lleno de amor. Registra los datos en el formulario y nosotros hacemos el resto.
          </p>
          
          <div class="hidden lg:flex items-center gap-2 text-[#1BB0B9] font-bold uppercase text-xs tracking-widest animate-pulse">
            <span>Completa el formulario</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
          </div>
        </div>

        <div class="w-full lg:w-7/12 bg-[#1BB0B9] rounded-3xl shadow-2xl relative overflow-hidden ring-8 ring-white/40">
          
          <div class="absolute top-0 right-0 w-40 h-40 bg-white/10 rounded-bl-full pointer-events-none"></div>

          <div class="p-6 md:p-8">
            
            <div class="mb-8">
              <h2 class="text-white text-3xl font-serif font-bold tracking-wide">
                Registro de Mascota
              </h2>
              <p class="text-[#BFF1F6] opacity-90 mt-1">Ingresa la información para encontrarle un hogar.</p>
            </div>

            <form @submit.prevent="handleSubmit" class="space-y-6">
              
              <div class="flex flex-col sm:flex-row gap-6">
                
                <div class="w-full sm:w-4/12 shrink-0">
                  <label class="label-standar">Fotografía</label>
                  <div class="relative aspect-square w-full bg-[#158f96] rounded-2xl border-2 border-dashed border-[#BFF1F6]/50 hover:border-[#BEDC74] hover:bg-[#138086] cursor-pointer group overflow-hidden transition-all shadow-inner flex flex-col items-center justify-center text-center p-4">
                    
                    <div v-if="!previewImage" class="flex flex-col items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mb-2 text-[#BFF1F6] group-hover:text-[#BEDC74] transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      <span class="text-xs text-white font-semibold">Subir Imagen</span>
                    </div>

                    <img v-else :src="previewImage" class="absolute inset-0 w-full h-full object-cover" />
                    <input type="file" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" @change="handleImageUpload" accept="image/*" />
                  </div>
                </div>

                <div class="w-full sm:w-8/12 grid grid-cols-2 gap-4 content-start">
                  <div class="col-span-2">
                    <label class="label-standar">Nombre</label>
                    <input type="text" class="form-input" placeholder="Ej. Max" />
                  </div>
                  
                  <div>
                    <label class="label-standar">Edad</label>
                    <input type="text" class="form-input" placeholder="Ej. 2 años" />
                  </div>
                  
                  <div class="relative">
                    <label class="label-standar">Categoría</label>
                    <select class="form-input appearance-none cursor-pointer">
                      <option>Perro</option>
                      <option>Gato</option>
                      <option>Hámster</option>
                      <option>Peces</option>
                      <option>Aves</option>
                    </select>
                    <div class="absolute right-3 top-[2.35rem] pointer-events-none text-gray-400">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
                    </div>
                  </div>

                  <div class="col-span-2 relative">
                     <label class="label-standar">Género</label>
                     <div class="flex gap-4 mt-1">
                        <label class="flex-1 cursor-pointer">
                          <input type="radio" name="gender" class="peer sr-only" />
                          <div class="bg-white/10 border border-white/30 text-white text-center py-3 rounded-xl peer-checked:bg-[#BEDC74] peer-checked:text-[#1a5f63] peer-checked:border-[#BEDC74] transition-all font-medium text-sm">
                            Macho
                          </div>
                        </label>
                        <label class="flex-1 cursor-pointer">
                          <input type="radio" name="gender" class="peer sr-only" />
                          <div class="bg-white/10 border border-white/30 text-white text-center py-3 rounded-xl peer-checked:bg-[#BEDC74] peer-checked:text-[#1a5f63] peer-checked:border-[#BEDC74] transition-all font-medium text-sm">
                            Hembra
                          </div>
                        </label>
                     </div>
                  </div>
                </div>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                <div>
                  <label class="label-standar">Teléfono </label>
                  <input type="tel" class="form-input" placeholder="+51 999 999 999" />
                </div>
                <div>
                  <label class="label-standar">Email (Opcional)</label>
                  <input type="email" class="form-input" placeholder="contacto@email.com" />
                </div>
              </div>

              <div>
                <label class="label-standar">Historia / Descripción</label>
                <textarea rows="3" class="form-input resize-none leading-relaxed" placeholder="Cuéntanos sobre su personalidad, gustos y por qué busca un hogar..."></textarea>
              </div>

              <div class="pt-2">
                <button type="submit" class="w-full bg-[#BEDC74] text-[#1a5f63] font-serif font-bold text-xl py-4 rounded-xl shadow-[0_10px_30px_-10px_rgba(190,220,116,0.5)] hover:bg-[#d4ed95] hover:shadow-[0_15px_35px_-10px_rgba(190,220,116,0.7)] hover:-translate-y-1 transition-all duration-300 flex items-center justify-center gap-3 group">
                  <span>Registrar Mascota</span>
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </button>
              </div>

            </form>
          </div>
        </div>

      </div>

      <!-- Sección de Listado de Mascotas -->
      <AdoptionList />

    </main>
    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useToast } from '@/composables/useToast';

const { addToast } = useToast();
import Header from './Header.vue';
import BackButton from '@/components/BackButton.vue';
import Footer from './Footer.vue';
import AdoptionList from '@/components/AdoptionList.vue';
import doghuella from '@/assets/images/doghuella.png';

const previewImage = ref(null);

const handleImageUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    previewImage.value = URL.createObjectURL(file);
  }
};

const handleSubmit = () => {
  addToast("¡Gracias por registrar la mascota! Nos pondremos en contacto contigo pronto para verificar los datos.", "success");
  console.log("Formulario enviado");
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');

.font-sans { font-family: 'Montserrat', sans-serif; }
.font-serif { font-family: 'Playfair Display', serif; }

/* Label estándar mejorado para legibilidad */
.label-standar {
  @apply block text-xs font-bold text-white/90 uppercase tracking-wider mb-1.5 ml-1;
}

/* Input cómodo: Buen tamaño de texto y padding */
.form-input {
  @apply w-full bg-white text-gray-800 rounded-xl px-4 py-3.5 text-sm md:text-base outline-none border-0 shadow-sm placeholder-gray-400 transition-all duration-200;
}

.form-input:focus {
  @apply ring-4 ring-[#BEDC74]/50 bg-white shadow-lg;
}
</style>