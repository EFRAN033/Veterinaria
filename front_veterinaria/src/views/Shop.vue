<template>
  <section id="shop" class="w-full py-24 px-4 md:px-16 bg-gray-50 font-sans relative overflow-hidden">
    
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
      <div class="absolute top-[-10%] right-[-5%] w-96 h-96 bg-[#02939E]/5 rounded-full blur-3xl"></div>
      <div class="absolute bottom-[-10%] left-[-5%] w-96 h-96 bg-[#a4ad74]/5 rounded-full blur-3xl"></div>
    </div>

    <div class="max-w-7xl mx-auto relative z-10">

      <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-6 mb-12">
        <div class="text-center sm:text-left flex-1">
          <span class="text-[#a4ad74] font-bold tracking-[0.2em] uppercase text-xs md:text-sm mb-3 block">
            Mima a tu mascota
          </span>
          <h2 class="app-type-title tracking-tight mb-6">
            Pet <span class="text-[#02939E]">Shop</span>
          </h2>
          <div class="w-16 h-1 bg-[#02939E] sm:mx-0 mx-auto rounded-full"></div>
        </div>
        <div class="flex justify-center sm:justify-end sm:pt-2 flex-shrink-0">
          <button
            type="button"
            class="flex items-center gap-2 px-4 py-2.5 bg-white border-2 border-gray-200 text-gray-800 font-bold text-sm uppercase tracking-wide hover:border-[#02939E] hover:text-[#02939E] transition-colors shadow-sm rounded-none focus:outline-none focus-visible:ring-2 focus-visible:ring-[#02939E]"
            aria-label="Abrir carrito de compras"
            @click="cartOpen = true"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.8" stroke="currentColor" class="w-5 h-5" aria-hidden="true">
              <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 00-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm12.75 0a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm-8.25-6.75h.008v.008H12v-.008zM12 18h.008v.008H12V18z" />
            </svg>
            Carrito
            <span
              v-if="cartItemCount > 0"
              class="min-w-[1.25rem] h-5 px-1 flex items-center justify-center bg-[#02939E] text-white text-xs font-bold rounded-full"
            >{{ cartItemCount }}</span>
          </button>
        </div>
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
          v-for="product in products" 
          :key="product.id" 
          class="group bg-white rounded-none shadow-sm hover:shadow-xl transition-all duration-500 ease-out overflow-hidden border border-gray-100 flex flex-col"
        >
          <div class="relative h-64 w-full bg-gray-100 overflow-hidden flex items-center justify-center p-4">
            <span v-if="product.discount" class="absolute top-3 left-3 bg-[#a4ad74] text-white text-[10px] font-bold px-2 py-1 rounded-md shadow-sm z-10">
              -{{ product.discount }}
            </span>
            
            <button
              type="button"
              class="absolute top-3 right-3 p-2 rounded-full bg-white/80 hover:bg-white transition-colors z-10 shadow-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-[#02939E] focus-visible:ring-offset-2"
              :class="isFavorite(product.id) ? 'text-red-500' : 'text-gray-400 hover:text-red-400'"
              :aria-pressed="isFavorite(product.id)"
              :aria-label="isFavorite(product.id) ? 'Quitar de favoritos' : 'Añadir a favoritos'"
              :title="isFavorite(product.id) ? 'Quitar de favoritos' : 'Guardar en favoritos'"
              @click.stop="toggleFavorite(product.id)"
            >
              <svg
                v-if="isFavorite(product.id)"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                class="w-5 h-5"
                fill="currentColor"
                aria-hidden="true"
              >
                <path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.691 2.25 5.353 4.814 3.25 7.875 3.25c1.227 0 2.363.436 3.248 1.217.885-.781 2.02-1.217 3.247-1.217 3.061 0 5.625 2.103 5.625 5.441 0 3.483-2.438 6.67-4.743 8.817a25.18 25.18 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z" />
              </svg>
              <svg
                v-else
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke-width="1.8"
                stroke="currentColor"
                class="w-5 h-5"
                aria-hidden="true"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9.12 8.098 9.12 8.098s9.12-.878 9.12-8.098z" />
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

            <h3 class="app-type-card-title text-gray-800 mb-1 group-hover:text-[#02939E] transition-colors">
              {{ product.name }}
            </h3>
            
            <div class="flex items-end gap-2 mb-4">
              <span class="text-xl font-bold text-[#02939E]">S/. {{ product.price }}</span>
              <span v-if="product.oldPrice" class="text-sm text-gray-400 line-through mb-1">S/. {{ product.oldPrice }}</span>
            </div>

            <button
              type="button"
              class="mt-auto w-full bg-gray-900 text-white py-3 rounded-none font-bold text-sm uppercase tracking-wider hover:bg-[#02939E] transition-colors duration-300 shadow-md hover:shadow-lg flex items-center justify-center gap-2 group-hover:translate-y-0"
              @click="addToCart(product)"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-4 h-4" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 10.5V6a3.75 3.75 0 10-7.5 0v4.5m11.356-1.993l1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 01-1.12-1.243l1.264-12A1.125 1.125 0 015.513 7.5h12.974c.576 0 1.059.435 1.119 1.007z" />
              </svg>
              Agregar
            </button>
          </div>
        </div>

      </div>

    </div>

    <!-- Carrito lateral -->
    <Teleport to="body">
      <Transition name="shop-cart-fade">
        <div
          v-if="cartOpen"
          class="fixed inset-0 z-[200] flex justify-end bg-black/40"
          role="dialog"
          aria-modal="true"
          aria-labelledby="shop-cart-title"
          @click.self="cartOpen = false"
        >
            <aside
              class="shop-cart-panel w-full max-w-md h-full bg-white shadow-2xl flex flex-col border-l border-gray-200"
              @click.stop
            >
              <div class="flex items-center justify-between p-4 border-b border-gray-200 bg-gray-50">
                <h3 id="shop-cart-title" class="text-lg font-bold text-gray-900">
                  Tu carrito
                </h3>
                <button
                  type="button"
                  class="p-2 text-gray-500 hover:text-gray-900 rounded-none focus:outline-none focus-visible:ring-2 focus-visible:ring-[#02939E]"
                  aria-label="Cerrar carrito"
                  @click="cartOpen = false"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div class="flex-1 overflow-y-auto p-4">
                <p v-if="cartLines.length === 0" class="text-gray-500 text-center py-12 text-sm">
                  Aún no hay productos. Pulsa <strong class="text-gray-700">Agregar</strong> en una tarjeta o usa el corazón para marcar favoritos.
                </p>
                <ul v-else class="space-y-4">
                  <li
                    v-for="line in cartLines"
                    :key="line.id"
                    class="flex gap-3 border border-gray-100 p-3 rounded-none bg-gray-50/80"
                  >
                    <img :src="line.image" :alt="line.name" class="w-16 h-16 object-contain bg-white border border-gray-100 flex-shrink-0" />
                    <div class="flex-1 min-w-0">
                      <p class="font-semibold text-gray-900 text-sm leading-tight line-clamp-2">{{ line.name }}</p>
                      <p class="text-[#02939E] font-bold text-sm mt-1">S/. {{ line.unitPrice.toFixed(2) }}</p>
                      <div class="flex items-center gap-2 mt-2">
                        <button
                          type="button"
                          class="w-8 h-8 border border-gray-300 bg-white font-bold text-gray-700 hover:bg-gray-100 rounded-none"
                          aria-label="Menos"
                          @click="changeCartQty(line.id, -1)"
                        >−</button>
                        <span class="text-sm font-semibold w-6 text-center">{{ line.qty }}</span>
                        <button
                          type="button"
                          class="w-8 h-8 border border-gray-300 bg-white font-bold text-gray-700 hover:bg-gray-100 rounded-none"
                          aria-label="Más"
                          @click="changeCartQty(line.id, 1)"
                        >+</button>
                        <button
                          type="button"
                          class="ml-auto text-xs text-red-600 font-semibold hover:underline"
                          @click="removeCartLine(line.id)"
                        >
                          Quitar
                        </button>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>

              <div v-if="cartLines.length > 0" class="border-t border-gray-200 p-4 bg-gray-50 space-y-3">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600">Subtotal</span>
                  <span class="font-bold text-gray-900">S/. {{ cartSubtotal.toFixed(2) }}</span>
                </div>
                <p class="text-xs text-gray-500">
                  El carrito se guarda en este dispositivo. El pago en línea se puede conectar más adelante.
                </p>
                <button
                  type="button"
                  class="w-full py-3 bg-[#02939E] text-white font-bold text-sm uppercase tracking-wide hover:bg-[#027a83] transition-colors rounded-none"
                  @click="cartOpen = false"
                >
                  Seguir comprando
                </button>
                <button
                  type="button"
                  class="w-full py-2 text-sm text-gray-600 font-semibold hover:text-red-600 rounded-none"
                  @click="clearCart"
                >
                  Vaciar carrito
                </button>
              </div>
            </aside>
        </div>
      </Transition>
    </Teleport>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue';
import camaCircularImage from '@/assets/images/cama_circular.svg';
import camaCestaImage from '@/assets/images/cama_cesta.svg';
import camaCuadradaImage from '@/assets/images/cama_cuadrada.svg';
import camaLiteraImage from '@/assets/images/cama_litera.svg';

const FAVORITES_STORAGE_KEY = 'fulness-petshop-favorites';
const CART_STORAGE_KEY = 'fulness-petshop-cart';

const products = [
  {
    id: 1,
    name: 'Cama Circular Premium',
    price: '30.00',
    oldPrice: '45.00',
    discount: '33%',
    rating: 5,
    reviews: 128,
    image: camaCircularImage,
  },
  {
    id: 2,
    name: 'Cama Cesta Tejida',
    price: '30.00',
    oldPrice: null,
    discount: null,
    rating: 4,
    reviews: 85,
    image: camaCestaImage,
  },
  {
    id: 3,
    name: 'Cama Cuadrada Soft',
    price: '30.00',
    oldPrice: '35.00',
    discount: '15%',
    rating: 5,
    reviews: 42,
    image: camaCuadradaImage,
  },
  {
    id: 4,
    name: 'Litera para Gatos',
    price: '30.00',
    oldPrice: null,
    discount: null,
    rating: 4,
    reviews: 67,
    image: camaLiteraImage,
  },
];

const cartOpen = ref(false);

function loadCartQuantities() {
  try {
    const raw = localStorage.getItem(CART_STORAGE_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return {};
    const out = {};
    for (const [k, v] of Object.entries(parsed)) {
      const qty = Number(v);
      if (qty > 0) out[Number(k)] = qty;
    }
    return out;
  } catch {
    return {};
  }
}

const cartQtyById = ref(loadCartQuantities());

function persistCart() {
  const cleaned = Object.fromEntries(
    Object.entries(cartQtyById.value).filter(([, q]) => Number(q) > 0),
  );
  try {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cleaned));
  } catch {
    /* ignore */
  }
}

const cartLines = computed(() => {
  return products
    .map((p) => {
      const qty = cartQtyById.value[p.id] || 0;
      if (qty <= 0) return null;
      const unitPrice = Number.parseFloat(String(p.price).replace(',', '.')) || 0;
      return {
        id: p.id,
        name: p.name,
        image: p.image,
        qty,
        unitPrice,
      };
    })
    .filter(Boolean);
});

const cartItemCount = computed(() =>
  Object.values(cartQtyById.value).reduce((sum, q) => sum + (Number(q) || 0), 0),
);

const cartSubtotal = computed(() =>
  cartLines.value.reduce((sum, line) => sum + line.unitPrice * line.qty, 0),
);

const addToCart = (product) => {
  const id = product.id;
  cartQtyById.value = {
    ...cartQtyById.value,
    [id]: (cartQtyById.value[id] || 0) + 1,
  };
  persistCart();
};

const changeCartQty = (id, delta) => {
  const current = cartQtyById.value[id] || 0;
  const next = Math.max(0, current + delta);
  const copy = { ...cartQtyById.value };
  if (next === 0) delete copy[id];
  else copy[id] = next;
  cartQtyById.value = copy;
  persistCart();
};

const removeCartLine = (id) => {
  const copy = { ...cartQtyById.value };
  delete copy[id];
  cartQtyById.value = copy;
  persistCart();
};

const clearCart = () => {
  cartQtyById.value = {};
  persistCart();
};

function loadFavoriteIds() {
  try {
    const raw = localStorage.getItem(FAVORITES_STORAGE_KEY);
    if (!raw) return new Set();
    const parsed = JSON.parse(raw);
    return new Set(Array.isArray(parsed) ? parsed.map(Number) : []);
  } catch {
    return new Set();
  }
}

const favoriteProductIds = ref(loadFavoriteIds());

const isFavorite = (id) => favoriteProductIds.value.has(id);

const toggleFavorite = (id) => {
  const next = new Set(favoriteProductIds.value);
  if (next.has(id)) next.delete(id);
  else next.add(id);
  favoriteProductIds.value = next;
  try {
    localStorage.setItem(FAVORITES_STORAGE_KEY, JSON.stringify([...next]));
  } catch {
    /* ignore quota / private mode */
  }
};

const activeCategory = ref('Camas');
const categories = ['Camas', 'Alimento', 'Juguetes', 'Ropa', 'Accesorios'];
</script>

<style scoped>
.shop-cart-fade-enter-active,
.shop-cart-fade-leave-active {
  transition: opacity 0.2s ease;
}
.shop-cart-fade-enter-from,
.shop-cart-fade-leave-to {
  opacity: 0;
}
</style>

<style>
@keyframes shop-cart-slide-in {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}
.shop-cart-panel {
  animation: shop-cart-slide-in 0.22s ease-out;
}
</style>