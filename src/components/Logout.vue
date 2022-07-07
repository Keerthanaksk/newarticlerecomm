<template>
    
    <button type="button" @click="logout" class="border btn btn-light btn-sm">Logout</button>

</template>

<script>

    import axios from 'axios'

    export default {
        name: 'Article',
        
        data() {
            return {
                loveCount: 0,
                test: ''
            }
        },

        methods: {
            async logout() {
                await axios({
                    method: 'post',
                    url: this.$store.state.API_BASE_URL + 'auth/logout',
                    withCredentials: true,
                })
                .then(
                    () => {
                        this.$store.commit('logout')
                        this.$router.push('/login')
                    }
                )
                .catch(res => console.log(res))
                
            },
        },
    }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
