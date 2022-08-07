import { createStore } from 'vuex'
import cookie from 'vue-cookies'

export default createStore({
    state () {
        return {
            email: cookie.get('email'),
            // backend api base url
            API_BASE_URL: process.env.VUE_APP_API_BASE_URL
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