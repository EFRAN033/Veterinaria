<template>
  <div class="min-h-screen bg-white font-sans text-gray-700 pb-20">
    <Header />
    
    <div class="pt-24 lg:pt-32 pb-12">
      <div class="container mx-auto px-4 max-w-7xl">
        <BackButton class="mb-8" />

        <div class="text-center mb-16 max-w-3xl mx-auto">
          <span class="text-[#1BB0B9] font-bold tracking-widest text-xs uppercase mb-3 block">Veterinaria & Estética</span>
          <h1 class="text-4xl lg:text-5xl font-serif font-bold text-gray-900 mb-6 leading-tight">
            Elige el cuidado ideal <br />
            para tu <span class="relative inline-block">
              mascota
              <svg class="absolute w-full h-3 -bottom-1 left-0 text-[#BEDC74]" viewBox="0 0 100 10" preserveAspectRatio="none">
                <path d="M0 5 Q 50 10 100 5" stroke="currentColor" stroke-width="3" fill="none" />
              </svg>
            </span>
          </h1>
          <p class="text-gray-500 text-lg">Selecciona una categoría abajo para personalizar la atención.</p>
        </div>

        <!-- Step Indicator -->
        <div class="max-w-3xl mx-auto mb-12">
          <div class="flex items-center justify-between relative">
            <div class="absolute left-0 top-1/2 -translate-y-1/2 w-full h-1 bg-gray-100 -z-10"></div>
            <div class="absolute left-0 top-1/2 -translate-y-1/2 h-1 bg-[#1BB0B9] transition-all duration-500 -z-10" :style="{ width: ((currentStep - 1) / 2) * 100 + '%' }"></div>
            
            <div v-for="step in 3" :key="step" class="flex flex-col items-center gap-2 bg-white px-2">
              <div 
                class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm transition-all duration-300 border-2"
                :class="currentStep >= step ? 'bg-[#1BB0B9] border-[#1BB0B9] text-white' : 'bg-white border-gray-200 text-gray-400'"
              >
                {{ step }}
              </div>
              <span class="text-xs font-bold uppercase tracking-wider" :class="currentStep >= step ? 'text-[#1BB0B9]' : 'text-gray-400'">
                {{ step === 1 ? 'Detalles' : step === 2 ? 'Fecha' : 'Confirmar' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Service Selection (Only visible in Step 1) -->
        <div v-if="currentStep === 1" class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-16">
          <button 
            v-for="service in serviceTypes" 
            :key="service.id"
            @click="selectedService = service.id"
            class="group relative flex flex-col items-center justify-center p-6 rounded-3xl transition-all duration-300 border-2"
            :class="selectedService === service.id 
              ? 'border-[#1BB0B9] bg-[#1BB0B9]/5 shadow-lg shadow-[#1BB0B9]/10' 
              : 'border-gray-100 bg-white hover:border-[#BEDC74] hover:shadow-md'"
          >
            <div class="mb-4 p-4 rounded-full transition-colors duration-300"
              :class="selectedService === service.id ? 'bg-[#1BB0B9] text-white' : 'bg-gray-50 text-gray-400 group-hover:bg-[#BEDC74]/20 group-hover:text-[#1a5f63]'">
              <svg v-if="service.id === 'consultation'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" /></svg>
              <svg v-if="service.id === 'general'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" /></svg>
              <svg v-if="service.id === 'clinical'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
              <svg v-if="service.id === 'aesthetic'" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
            </div>
            <span class="font-bold text-sm tracking-wide" :class="selectedService === service.id ? 'text-[#1BB0B9]' : 'text-gray-500'">{{ service.name }}</span>
            
            <div v-if="selectedService === service.id" class="absolute top-3 right-3 text-[#1BB0B9] animate-bounce-small">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg>
            </div>
          </button>
        </div>

        <div class="flex flex-col lg:flex-row gap-12 relative">
          
          <div class="flex-1 min-w-0">
            <Transition name="fade" mode="out-in">
              
              <!-- STEP 1: Service Details Forms -->
              <div v-if="currentStep === 1">
                <div v-if="selectedService === 'consultation'" key="consultation" class="space-y-10">
                <div class="border-l-4 border-[#1BB0B9] pl-6">
                  <h2 class="text-3xl font-serif font-bold text-gray-900">Detalles de la Consulta</h2>
                  <p class="text-gray-500 mt-1">Cuéntanos qué le sucede a tu mascota.</p>
                </div>

                <form @submit.prevent="handleStep1Submit" id="mainForm" class="space-y-8">
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div class="group relative">
                      <input type="text" v-model="consultation.petName" placeholder=" " class="floating-input peer" />
                      <label class="floating-label">Nombre de la Mascota</label>
                    </div>
                    <div class="group relative">
                      <select v-model="consultation.species" class="floating-input peer pt-6 pb-2">
                        <option value="" disabled selected></option>
                        <option value="perro">Perro</option>
                        <option value="gato">Gato</option>
                        <option value="ave">Ave</option>
                        <option value="hamster">Hámster</option>
                        <option value="pez">Pez</option>
                      </select>
                      <label class="floating-label">Especie</label>
                    </div>
                  </div>

                  <div class="group relative">
                    <textarea v-model="consultation.symptoms" rows="4" placeholder=" " class="floating-input peer resize-none"></textarea>
                    <label class="floating-label">Síntomas Principales</label>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div class="group relative">
                       <select v-model="consultation.duration" class="floating-input peer pt-6 pb-2">
                        <option value="" disabled selected></option>
                        <option value="horas">Menos de 24 horas</option>
                        <option value="dias">1-3 días</option>
                        <option value="semana">Más de una semana</option>
                      </select>
                      <label class="floating-label">Duración</label>
                    </div>
                    
                    <div>
                      <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-3">Nivel de Urgencia</label>
                      <div class="flex gap-4">
                        <label v-for="level in ['baja', 'media', 'alta']" :key="level" class="flex-1 cursor-pointer">
                          <input type="radio" v-model="consultation.urgency" :value="level" class="hidden peer">
                          <div class="py-3 px-4 rounded-xl border-2 border-gray-100 text-center capitalize font-bold text-gray-400 transition-all peer-checked:border-[#1BB0B9] peer-checked:text-[#1BB0B9] peer-checked:bg-[#1BB0B9]/5 hover:bg-gray-50">
                            {{ level }}
                          </div>
                        </label>
                      </div>
                    </div>
                  </div>

                  <div>
                    <label class="block text-xs font-bold text-gray-400 uppercase tracking-wider mb-4">Fotos de evidencia</label>
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
                      <div v-for="i in 4" :key="i" @click="triggerFileInput(i)"
                        class="aspect-square rounded-2xl border-2 border-dashed border-gray-200 hover:border-[#1BB0B9] hover:bg-[#1BB0B9]/5 cursor-pointer flex items-center justify-center transition-all overflow-hidden relative group">
                        <template v-if="evidencePreviews[i]">
                          <img :src="evidencePreviews[i]" class="w-full h-full object-cover" />
                          <div class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-white">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                          </div>
                        </template>
                        <template v-else>
                          <svg class="w-8 h-8 text-gray-300 group-hover:text-[#1BB0B9] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                        </template>
                        <input type="file" accept="image/*" class="hidden" :ref="'fileInput' + i" @change="handleFileChange($event, i)" />
                      </div>
                    </div>
                  </div>
                </form>
              </div>

              <div v-else-if="selectedService === 'general'" key="general" class="space-y-10">
                <div class="border-l-4 border-[#1BB0B9] pl-6">
                  <h2 class="text-3xl font-serif font-bold text-gray-900">Servicios Generales</h2>
                  <p class="text-gray-500 mt-1">Mantenimiento y prevención.</p>
                </div>

                <form @submit.prevent="handleStep1Submit" id="mainForm" class="space-y-8">
                  <div class="grid grid-cols-1 gap-8">
                     <div class="group relative">
                      <select v-model="general.serviceType" class="floating-input peer pt-6 pb-2">
                        <option value="" disabled selected></option>
                        <option value="vacunacion">Vacunación</option>
                        <option value="desparasitacion">Desparasitación</option>
                        <option value="revision">Revisión General</option>
                        <option value="limpieza">Limpieza Dental</option>
                        <option value="cirugia">Cirugía Menor</option>
                      </select>
                      <label class="floating-label">Tipo de Servicio</label>
                    </div>

                    <!-- Removed preferredDate input as it's now in Step 2 -->
                    
                    <div class="group relative">
                      <textarea v-model="general.notes" rows="4" placeholder=" " class="floating-input peer resize-none"></textarea>
                      <label class="floating-label">Indicaciones Generales</label>
                    </div>
                  </div>
                </form>
              </div>

              <div v-else-if="selectedService === 'clinical'" key="clinical" class="space-y-10">
                 <div class="border-l-4 border-[#1BB0B9] pl-6">
                  <h2 class="text-3xl font-serif font-bold text-gray-900">Caso Clínico</h2>
                  <p class="text-gray-500 mt-1">Información detallada para diagnósticos complejos.</p>
                </div>

                <form @submit.prevent="handleStep1Submit" id="mainForm" class="space-y-8">
                   <div class="group relative">
                    <textarea v-model="clinical.description" rows="6" placeholder=" " class="floating-input peer resize-none"></textarea>
                    <label class="floating-label">Descripción del Caso</label>
                  </div>

                  <div class="group relative">
                    <textarea v-model="clinical.history" rows="4" placeholder=" " class="floating-input peer resize-none"></textarea>
                    <label class="floating-label">Antecedentes Médicos</label>
                  </div>

                  <div class="flex flex-col gap-4">
                    <label class="flex items-center gap-3 p-4 border border-gray-200 rounded-xl cursor-pointer hover:bg-gray-50 transition-colors">
                      <input type="checkbox" v-model="clinical.isFollowUp" class="w-5 h-5 accent-[#1BB0B9]">
                      <span class="font-bold text-gray-700">¿Es una cita de control?</span>
                    </label>

                    <div v-if="clinical.isFollowUp" class="group relative mt-2 animate-fade-in-down">
                      <input type="text" v-model="clinical.previousCase" placeholder=" " class="floating-input peer" />
                      <label class="floating-label">Número de Caso Anterior</label>
                    </div>
                  </div>
                </form>
              </div>

              <div v-else-if="selectedService === 'aesthetic'" key="aesthetic" class="space-y-10">
                 <div class="border-l-4 border-[#1BB0B9] pl-6">
                  <h2 class="text-3xl font-serif font-bold text-gray-900">Estética & Spa</h2>
                  <p class="text-gray-500 mt-1">Belleza y cuidado para tu mejor amigo.</p>
                </div>

                <form @submit.prevent="handleStep1Submit" id="mainForm" class="space-y-10">
                   <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                      <div class="group relative">
                        <input type="text" v-model="aesthetic.petName" placeholder=" " class="floating-input peer" />
                        <label class="floating-label">Nombre de la Mascota</label>
                      </div>
                      <div class="group relative">
                        <input type="text" v-model="aesthetic.breed" placeholder=" " class="floating-input peer" />
                        <label class="floating-label">Raza</label>
                      </div>
                      <div class="group relative">
                        <select v-model="aesthetic.species" class="floating-input peer pt-6 pb-2">
                          <option value="" disabled selected></option>
                          <option value="perro">Perro</option>
                          <option value="gato">Gato</option>
                        </select>
                        <label class="floating-label">Especie</label>
                      </div>
                    </div>

                    <div class="space-y-6">
                      <div v-for="(item, index) in aesthetic.services" :key="index" class="p-6 rounded-3xl bg-gray-50 border border-gray-100 relative">
                         <div class="flex justify-between items-start mb-6">
                           <h3 class="font-bold text-gray-800 text-lg">Servicio #{{ index + 1 }}</h3>
                           <button v-if="aesthetic.services.length > 1" @click="removeService(index)" type="button" class="text-red-400 hover:text-red-600">
                             <span class="text-sm font-bold">Eliminar</span>
                           </button>
                         </div>

                         <div class="grid gap-6">
                           <div class="group relative bg-white rounded-xl">
                              <select v-model="item.type" class="floating-input peer pt-6 pb-2 bg-white">
                                <option value="" disabled selected></option>
                                <option value="baño">Baño Completo</option>
                                <option value="corte">Corte de Pelo</option>
                                <option value="baño-corte">Baño + Corte</option>
                                <option value="uñas">Corte de Uñas</option>
                                <option value="limpieza-oidos">Limpieza de Oídos</option>
                              </select>
                              <label class="floating-label bg-white">Tipo de Servicio</label>
                            </div>
                            
                            <div class="group relative bg-white rounded-xl">
                              <textarea v-model="item.instructions" rows="2" placeholder=" " class="floating-input peer resize-none bg-white"></textarea>
                              <label class="floating-label bg-white">Instrucciones Especiales</label>
                            </div>
                         </div>
                      </div>

                      <button @click="addService" type="button" class="w-full py-4 border-2 border-dashed border-gray-300 rounded-2xl text-gray-500 font-bold hover:border-[#1BB0B9] hover:text-[#1BB0B9] transition-all flex items-center justify-center gap-2">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" /></svg>
                        Agregar otro servicio
                      </button>
                    </div>
                </form>
              </div>

              </div>

              <!-- STEP 2: Date & Time -->
              <div v-else-if="currentStep === 2" key="datetime">
                <DateTimePicker v-model="dateTime" />
              </div>

              <!-- STEP 3: Confirmation -->
              <div v-else-if="currentStep === 3" key="summary">
                <ServiceSummary 
                  :serviceType="selectedService"
                  :details="currentServiceDetails"
                  :dateTime="dateTime"
                  :estimatedCost="estimatedCost"
                  @edit="goToStep"
                />
              </div>

            </Transition>
          </div>

          <div class="lg:w-1/3">
            <div class="sticky top-8 space-y-6">
              
              <div class="bg-white rounded-3xl p-8 shadow-2xl relative overflow-hidden border-2 border-gray-100">
                <div class="absolute top-0 right-0 w-32 h-32 bg-[#1BB0B9] rounded-full blur-[60px] opacity-10"></div>
                <div class="absolute bottom-0 left-0 w-24 h-24 bg-[#BEDC74] rounded-full blur-[40px] opacity-10"></div>

                <div class="relative z-10">
                  <h3 class="text-gray-500 font-medium mb-1 uppercase tracking-wider text-xs">Total Estimado</h3>
                  <div class="flex items-baseline gap-1 mb-6">
                    <span class="text-2xl text-[#1BB0B9]">S/.</span>
                    <span class="text-6xl font-serif font-bold tracking-tighter text-gray-900">{{ estimatedCost }}</span>
                  </div>

                  <div class="border-t border-gray-200 pt-6 mb-8 space-y-3">
                    <div class="flex justify-between text-sm text-gray-500">
                      <span>Servicio Base</span>
                      <span>Incluido</span>
                    </div>
                     <div class="flex justify-between text-sm text-gray-500">
                      <span>Impuestos</span>
                      <span>Calculado al final</span>
                    </div>
                  </div>

                  <button 
                    v-if="currentStep === 1"
                    @click="triggerSubmit"
                    class="w-full py-4 bg-[#1BB0B9] hover:bg-[#16a0a8] text-white font-bold rounded-xl transition-all shadow-lg hover:shadow-[#1BB0B9]/40 active:scale-95 flex items-center justify-center gap-2 group"
                  >
                    <span>Continuar</span>
                    <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                  </button>

                  <button 
                    v-else-if="currentStep === 2"
                    @click="nextStep"
                    class="w-full py-4 bg-[#1BB0B9] hover:bg-[#16a0a8] text-white font-bold rounded-xl transition-all shadow-lg hover:shadow-[#1BB0B9]/40 active:scale-95 flex items-center justify-center gap-2 group"
                  >
                    <span>Revisar Solicitud</span>
                    <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                  </button>

                  <button 
                    v-else
                    @click="submitRequest"
                    :disabled="loading"
                    class="w-full py-4 bg-[#1BB0B9] hover:bg-[#16a0a8] text-white font-bold rounded-xl transition-all shadow-lg hover:shadow-[#1BB0B9]/40 active:scale-95 flex items-center justify-center gap-2 group disabled:opacity-70 disabled:cursor-not-allowed disabled:transform-none"
                  >
                    <span v-if="loading" class="animate-spin mr-2">⌛</span>
                    <span v-if="loading">Enviando...</span>
                    <span v-else>Confirmar Solicitud</span>
                    <svg v-if="!loading" class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                  </button>
                  
                  <button 
                    v-if="currentStep > 1"
                    @click="prevStep"
                    class="w-full mt-3 py-3 text-gray-400 font-bold hover:text-gray-600 transition-colors"
                  >
                    Atrás
                  </button>
                  
                  <p class="text-center text-gray-400 text-xs mt-4">*Pago presencial o vía App</p>
                </div>
              </div>

              <div class="bg-[#F3F4F6] rounded-3xl p-6 border border-gray-100 hidden lg:block">
                <div class="flex items-start gap-4">
                  <div class="bg-white p-3 rounded-full shadow-sm text-[#1BB0B9]">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  </div>
                  <div>
                    <h4 class="font-bold text-gray-800 mb-1">¿Necesitas ayuda?</h4>
                    <p class="text-sm text-gray-500 leading-relaxed">
                      Si tienes dudas sobre qué servicio elegir, contáctanos directamente al WhatsApp.
                    </p>
                    <a href="#" class="text-[#1BB0B9] text-sm font-bold mt-2 inline-block hover:underline">Chat con Soporte &rarr;</a>
                  </div>
                </div>
              </div>

            </div>
          </div>

        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import Header from './Header.vue';
import BackButton from '@/components/BackButton.vue';
import DateTimePicker from '@/components/DateTimePicker.vue';
import ServiceSummary from '@/components/ServiceSummary.vue';
import { useServiceRequests } from '@/composables/useServiceRequests';
import { useToast } from '@/composables/useToast';

const router = useRouter();
const { createServiceRequest, loading, error } = useServiceRequests();
const { addToast } = useToast();

const currentStep = ref(1);
const selectedService = ref('consultation');
const dateTime = ref({ date: null, timeSlot: '', isUrgent: false });

const serviceTypes = [
  { id: 'consultation', name: 'Consulta' },
  { id: 'general', name: 'General' },
  { id: 'clinical', name: 'Clínico' },
  { id: 'aesthetic', name: 'Estética' }
];

const triggerSubmit = () => {
  const form = document.getElementById('mainForm');
  if (form) form.requestSubmit();
};

const evidencePreviews = ref({});

const triggerFileInput = (index) => {
  const inputs = document.querySelectorAll('input[type="file"]');
  if (inputs[index - 1]) inputs[index - 1].click();
};

const handleFileChange = (event, index) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      evidencePreviews.value[index] = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const consultation = ref({ petName: '', species: '', symptoms: '', duration: '', urgency: '' });
const general = ref({ serviceType: '', petName: '', preferredDate: '', notes: '' });
const clinical = ref({ description: '', history: '', isFollowUp: false, previousCase: '' });
const aesthetic = ref({ petName: '', breed: '', services: [{ type: '', instructions: '' }] });

const addService = () => {
  aesthetic.value.services.push({ type: '', instructions: '' });
};

const removeService = (index) => {
  aesthetic.value.services.splice(index, 1);
};

const estimatedCost = computed(() => {
  let cost = 0;
  switch(selectedService.value) {
    case 'consultation':
      cost = 50;
      if (consultation.value.urgency === 'alta') cost += 30;
      break;
    case 'general':
      const serviceCosts = { 'vacunacion': 40, 'desparasitacion': 30, 'revision': 50, 'limpieza': 80, 'cirugia': 200 };
      cost = serviceCosts[general.value.serviceType] || 0;
      break;
    case 'clinical':
      cost = 100;
      if (clinical.value.isFollowUp) cost = 60;
      break;
    case 'aesthetic':
      aesthetic.value.services.forEach(service => {
        const aestheticCosts = { 'baño': 40, 'corte': 50, 'baño-corte': 80, 'uñas': 20, 'limpieza-oidos': 25 };
        cost += aestheticCosts[service.type] || 0;
      });
      break;
  }
  return cost;
});

const currentServiceDetails = computed(() => {
  switch(selectedService.value) {
    case 'consultation': return consultation.value;
    case 'general': return general.value;
    case 'clinical': return clinical.value;
    case 'aesthetic': return aesthetic.value;
    default: return {};
  }
});

const nextStep = () => {
  if (currentStep.value === 1) {
    const form = document.getElementById('mainForm');
    if (form && !form.checkValidity()) {
      form.reportValidity();
      return;
    }
    currentStep.value = 2;
  } else if (currentStep.value === 2) {
    if (!dateTime.value.isUrgent && (!dateTime.value.date || !dateTime.value.timeSlot)) {
      addToast('Por favor selecciona una fecha y hora, o marca la opción de urgencia.', 'warning');
      return;
    }
    currentStep.value = 3;
  }
};

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--;
  }
};

const goToStep = (step) => {
  currentStep.value = step;
};

const submitRequest = async () => {
  try {
    const commonData = {
      estimated_cost: estimatedCost.value,
      service_data: {
        ...currentServiceDetails.value,
        preferredDate: dateTime.value.date,
        preferredTime: dateTime.value.timeSlot,
        isUrgent: dateTime.value.isUrgent
      },
      images: selectedService.value === 'consultation' ? Object.values(evidencePreviews.value).filter(img => img) : []
    };

    let requestData = { ...commonData, service_type: selectedService.value };

    if (selectedService.value === 'consultation') {
      requestData.pet_name = consultation.value.petName;
    } else if (selectedService.value === 'general') {
      requestData.pet_name = general.value.petName;
      delete requestData.service_data.preferredDate; 
      requestData.service_data.preferredDate = dateTime.value.date; // Ensure new one is used
    } else if (selectedService.value === 'aesthetic') {
      requestData.pet_name = aesthetic.value.petName;
    } else if (selectedService.value === 'clinical') {
      // Clinical request doesn't have a specific pet name field in the current form
      // We could add it, but for now we'll send it without if not present
      // or we could assume it's part of the description
    }

    await createServiceRequest(requestData);
    addToast('Solicitud enviada exitosamente. Te contactaremos pronto.', 'success');
    
    router.push('/home');
  } catch (err) {
    console.error(err);
    addToast('Error al enviar solicitud. Por favor intenta nuevamente.', 'error');
  }
};

const handleStep1Submit = () => {
  nextStep();
};


</script>

<style scoped>
/* ESTILO FLOATING LABELS (Material Design Moderno) */
.floating-input {
  @apply block px-4 pb-2.5 pt-5 w-full text-gray-900 bg-gray-50 border-2 border-gray-100 rounded-xl appearance-none focus:outline-none focus:ring-0 focus:border-[#1BB0B9] focus:bg-white transition-all;
}

.floating-label {
  @apply absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] left-4 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 peer-focus:text-[#1BB0B9] pointer-events-none font-bold;
}

/* Transiciones de Fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.animate-bounce-small {
  animation: bounce-small 2s infinite;
}

@keyframes bounce-small {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-25%); }
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-down {
  animation: fadeInDown 0.3s ease-out forwards;
}
</style>