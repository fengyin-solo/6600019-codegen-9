import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './style.css'
import { useSeismicStore } from './store/seismic'

const app = createApp(App).use(createPinia())

const store = useSeismicStore()
store.loadFavorites()

app.mount('#app')
