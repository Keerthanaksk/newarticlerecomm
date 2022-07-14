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

async function getCurrentUser() {
    return (
        await fetch(
            store.state.API_BASE_URL + `user/current-user`,
            {
                method: 'GET',
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Credetials": "true",
                },
                credentials: 'include',
            }
        )
        .then(async res => 
            {
                if(res.status == 200) {
                    const jsonValue = await res.json()
                    return Promise.resolve(jsonValue)
                } else {
                    return Promise.reject('Error')
                }
            }
        )
        .then(res => res.email)
        .catch(() => {
            return {name: 'Login'}
        })
    )
}

router.beforeEach( async (to,) => {
    
    
    const currentUserEmail = await getCurrentUser()

    const loggedIn = (currentUserEmail === store.state.email)
    
    if(!loggedIn) {
        // Redir to login if not authenticated 
        // and is trying to access other routes
        if (to.name !== 'Login') {
            return {name: 'Login'}
        }
    } else if (loggedIn && to.name == 'Login'){
        // prevent accessing Login route when authenticated
        return {name: 'Home'}
    }
    
})

export default router