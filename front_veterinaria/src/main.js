import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia'; // <-- Import createPinia

import './assets/css/main.css'; // Your original correct path

const app = createApp(App);
const pinia = createPinia(); // <-- Create Pinia instance

app.use(pinia); // <-- Use Pinia
app.use(router);

app.mount('#app');