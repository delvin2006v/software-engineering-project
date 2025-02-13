import { createApp } from 'vue'
import './index.css'
import App from './App.vue'
import routers from './routers/routers'
import store from './store/vuex'

const app = createApp(App)

app.use(routers)
app.use(store)

app.mount('#app')