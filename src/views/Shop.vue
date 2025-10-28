<template>
    <section id="shop" class="w-full py-20 px-4 md:px-12 bg-[#02939E]/10 relative overflow-hidden">
      
      <div class="absolute inset-0 z-0 opacity-60">
        <div class="absolute top-10 left-10 w-12 h-12 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat"></div>
        <div class="absolute top-1/3 right-1/4 w-16 h-16 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat rotate-45"></div>
        <div class="absolute bottom-20 left-1/2 w-20 h-20 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat -rotate-45"></div>
        <div class="absolute top-1/4 left-1/2 w-24 h-24 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat"></div>
        <div class="absolute bottom-10 right-10 w-12 h-12 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat"></div>
        <div class="absolute top-1/2 left-1/4 w-16 h-16 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat rotate-90"></div>
        <div class="absolute top-3/4 left-1/3 w-12 h-12 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat rotate-12"></div>
        <div class="absolute top-10 right-10 w-20 h-20 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat -rotate-12"></div>
        <div class="absolute bottom-1/4 left-1/4 w-16 h-16 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat rotate-45"></div>
        <div class="absolute bottom-10 left-3/4 w-12 h-12 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat"></div>
        <div class="absolute top-1/2 right-1/2 w-24 h-24 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat rotate-[60deg]"></div>
        <div class="absolute bottom-1/3 left-10 w-16 h-16 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat -rotate-45"></div>
        
        <div class="absolute top-1/4 right-1/2 w-12 h-12 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat rotate-12"></div>
        <div class="absolute bottom-1/4 right-10 w-16 h-16 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat -rotate-12"></div>
        <div class="absolute top-20 right-1/3 w-20 h-20 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat rotate-45"></div>
        <div class="absolute bottom-1/2 left-1/3 w-12 h-12 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat -rotate-45"></div>
        <div class="absolute top-3/4 right-1/4 w-16 h-16 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat"></div>
        <div class="absolute top-1/3 left-1/3 w-20 h-20 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat rotate-90"></div>
        <div class="absolute bottom-10 right-1/3 w-12 h-12 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat"></div>
        <div class="absolute top-10 left-1/3 w-16 h-16 bg-[url('@/assets/images/catpatas.png')] bg-contain bg-no-repeat rotate-12"></div>
      </div>
  
      <div class="max-w-7xl mx-auto relative z-10">
  
        <div class="text-center mb-12">
          <h2 class="text-5xl md:text-6xl font-sans font-light text-gray-800 tracking-widest uppercase">
            Pet Shop
          </h2>
        </div>
  
        <div class="flex flex-wrap justify-center gap-4 mb-16">
          <button class="bg-[#83CFD4] text-white px-6 py-2 rounded-full shadow-md hover:bg-[#6abfc3] transition duration-300">Camas</button>
          <button class="bg-white text-gray-700 px-6 py-2 rounded-full shadow-md hover:bg-gray-100 transition duration-300">Alimento</button>
          <button class="bg-white text-gray-700 px-6 py-2 rounded-full shadow-md hover:bg-gray-100 transition duration-300">Juguetes</button>
          <button class="bg-white text-gray-700 px-6 py-2 rounded-full shadow-md hover:bg-gray-100 transition duration-300">Ropa</button>
          <button class="bg-white text-gray-700 px-6 py-2 rounded-full shadow-md hover:bg-gray-100 transition duration-300">Accesorios</button>
          <a href="#" class="ml-4 flex items-center text-gray-700 font-semibold uppercase hover:underline">VER TODO</a>
        </div>
  
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
          
          <div class="bg-white rounded-2xl shadow-xl overflow-hidden p-4 flex flex-col items-center text-center transition-all duration-300 hover:shadow-2xl">
            <img :src="camaCircularImage" alt="Cama circular" class="w-full h-48 object-cover rounded-md mb-4">
            <div class="flex text-yellow-500 mb-2">
              <span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">★</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-1">Cama circular</h3>
            <p class="text-sm text-gray-600 mb-2">15% dstco</p>
            <p class="text-2xl font-bold text-gray-900 mb-4">S/. 30.00</p>
            <button class="bg-[#5AD9E0] text-white px-6 py-2 rounded-full hover:bg-[#4ac3cc] transition duration-300">Agregar</button>
          </div>
  
          <div class="bg-white rounded-2xl shadow-xl overflow-hidden p-4 flex flex-col items-center text-center transition-all duration-300 hover:shadow-2xl">
            <img :src="camaCestaImage" alt="Cama cesta" class="w-full h-48 object-cover rounded-md mb-4">
            <div class="flex text-yellow-500 mb-2">
              <span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">☆</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-1">Cama cesta</h3>
            <p class="text-sm text-gray-600 mb-2">1Skin% dstco</p>
            <p class="text-2xl font-bold text-gray-900 mb-4">S/. 30.00</p>
            <button class="bg-[#5AD9E0] text-white px-6 py-2 rounded-full hover:bg-[#4ac3cc] transition duration-300">Agregar</button>
          </div>
  
          <div class="bg-white rounded-2xl shadow-xl overflow-hidden p-4 flex flex-col items-center text-center transition-all duration-300 hover:shadow-2xl">
            <img :src="camaCuadradaImage" alt="Cama cuadrada" class="w-full h-48 object-cover rounded-md mb-4">
            <div class="flex text-yellow-500 mb-2">
              <span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">☆</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-1">Cama cuadrada</h3>
            <p class="text-sm text-gray-600 mb-2">15% dstco</p>
            <p class="text-2xl font-bold text-gray-900 mb-4">S/. 30.00</p>
            <button class="bg-[#5AD9E0] text-white px-6 py-2 rounded-full hover:bg-[#4ac3cc] transition duration-300">Agregar</button>
          </div>
  
          <div class="bg-white rounded-2xl shadow-xl overflow-hidden p-4 flex flex-col items-center text-center transition-all duration-300 hover:shadow-2xl">
            <img :src="camaLiteraImage" alt="Cama litera" class="w-full h-48 object-cover rounded-md mb-4">
            <div class="flex text-yellow-500 mb-2">
              <span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">★</span><span class="text-lg">☆</span>
            </div>
            <h3 class="text-xl font-semibold text-gray-800 mb-1">Cama litera</h3>
            <p class="text-sm text-gray-600 mb-2">15% dstco</p>
            <p class="text-2xl font-bold text-gray-900 mb-4">S/. 30.00</p>
            <button class="bg-[#5AD9E0] text-white px-6 py-2 rounded-full hover:bg-[#4ac3cc] transition duration-300">Agregar</button>
          </div>
  
        </div>
  
      </div>
    </section>
  </template>
  
  <script setup>
  // Las imágenes de los productos SÍ son .svg
  import camaCircularImage from '@/assets/images/cama_circular.svg';
  import camaCestaImage from '@/assets/images/cama_cesta.svg';
  import camaCuadradaImage from '@/assets/images/cama_cuadrada.svg';
  import camaLiteraImage from '@/assets/images/cama_litera.svg';
  
  // La huella (catpatas.png) no necesita importarse aquí 
  // porque la estamos llamando directamente desde el CSS de Tailwind
  </script>
  
  <style scoped>
  /* Puedes añadir estilos específicos aquí si lo necesitas */
  </style>