<template>
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-5">
                <div class="card border-0 shadow mt-5">
                    <div class="card-body p-5">
                        
                        <h1 class="card-title display-6 text-center fw-bolder">Welcome Back!</h1>
                        <h6 class="card-subtitle mb-4 text-muted text-center">Intelligent Newsletter by UnionBank and Aboitiz</h6>
                        
                        <form method="POST" @submit.prevent="login">
                            <div class="mb-3">
                                <label class="form-label">Email</label>
                                <input type="email" class="form-control" v-model="email">
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Password</label>
                                <input type="password" class="form-control" v-model="password">
                            </div>
                            <div class="d-grid gap-2">
                                <button class="btn btn-warning text-light fw-bolder" type="submit">Login account</button>
                            </div>
                        </form>
                        
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
    import axios from 'axios'
    import qs from 'qs';

    export default {
        name: 'Login',
        data() {
            return {
                email: '',
                password: ''
            }
        },

        methods: {
            async login() {
                // var bodyFormData = new FormData();
                // bodyFormData.append('username', this.email);
                // bodyFormData.append('password', this.password);
                const data = {'username': this.email, 'password': this.password}

                await axios({
                    method: 'post',
                    url: this.$store.state.API_BASE_URL + 'auth/login',
                    data: qs.stringify(data),
                    withCredentials: true,
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
                })
                .then( res => {
                        
                        this.$store.commit('login', res.data['email'])
                        this.$router.push('/')
                        
                    }
                )
                .catch(res => console.log(res));
            }
        }
    }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  
</style>
