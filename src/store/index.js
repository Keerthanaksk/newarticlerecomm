import { createStore } from 'vuex'
import cookie from 'vue-cookies'

export default createStore({
    state () {
        return {
            username: cookie.get('username'),
            authenticated: cookie.get('authenticated') === 'true',
        }
    },
    mutations: {
        login (state, username) {
            cookie.set('username', username)
            state.username = username

            cookie.set('authenticated', true)
            state.authenticated = true

        },
        logout (state) {
            cookie.remove('username')
            state.username = ''

            cookie.remove('authenticated')
            state.authenticated = false
        }
    }
}
)