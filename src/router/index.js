import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'

import Home from '../views/Home.vue'
import Login from '../views/Login.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

router.beforeEach( (to,) => {
    const authenticated = store.state.authenticated 
    
    // Redir to login if not authenticated and tries to access other routes
    // else if prevent accessing Login when authenticated
    if (!authenticated && to.name !== 'Login' ) {
        return {name: 'Login'}
    } else if (authenticated && to.name == 'Login') {
        return {name: 'Home'}
    }
    
})

export default router