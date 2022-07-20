import { createStore } from 'vuex'
import cookie from 'vue-cookies'

export default createStore({
    state () {
        return {
            email: cookie.get('email'),
            // API_BASE_URL: 'http://localhost:8080/'
            API_BASE_URL: process.env.VUE_APP_ENV == 'prod' ? process.env.VUE_APP_API_BASE_URL : 'http://localhost:8080/'
        }
    },
    mutations: {
        login (state, email) {
            cookie.set('email', email)
            state.email = email

        },
        logout (state) {
            cookie.remove('email')
            state.email = ''
        }
    }
}
)