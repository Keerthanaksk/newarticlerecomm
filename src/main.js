import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

import 'bootstrap/dist/css/bootstrap.min.css'
import "bootstrap/dist/js/bootstrap.bundle.js"
import 'bootstrap-icons/font/bootstrap-icons.css'

createApp(App)
.use(router)
.use(store)
.mount('#app')

// import 'bootstrap/dist/js/bootstrap.bundle.js'
