<template>
    
    <div class="card shadow border-0">
        <!-- <img :src="randomPic" class="card-img-top"> -->
        <h5 class="card-header">{{this.title}}</h5>
        <div class="card-body">
            <div class="d-flex">
                
                <div class="d-flex flex-column align-items-center align-self-center">
                    <i :class="'bi ' + (this.loved ? 'bi-heart-fill text-danger' : 'bi-heart')" @click="love"></i>
                    <span></span>
                    <!-- <span>{{this.loved}}</span> -->
                </div>
                <div class="ms-4">
                    <!-- <h5 class="card-title">{{this.title}}</h5> -->
                    <p class="card-text">{{this.summary}}</p>
                    <div class="d-flex justify-content-between">
                        <a :href="this.link" target="_blank" class="small text-muted align-self-end" @click="linkClick">Click to read more</a>
                        <span v-if="this.clicks" class="small text-muted"> <b>{{this.clicks}}</b> user(s) have clicked this article!</span>

                    </div>
                </div>
            </div>
                    
        </div>
    </div>

</template>

<script>

    // import axios from 'axios'

    export default {
        name: 'Article',
        
        data() {
            return {
                loves: 0,
                loved: false
            }
        },

        props: {
            id: String,
            title: String,
            link: String,
            summary: String,
            clickCounts: Number,
            isLoved: Boolean
        },

        created() {
            this.clicks = this.clickCounts
            this.loved = this.isLoved
        },

        computed: {
            randomPic() {
                return `https://picsum.photos/seed/` + Math.floor(Math.random() * 100) + `/600/400`
            }
        },

        methods: {
            async linkClick() {
                await fetch(
                    this.$store.state.API_BASE_URL 
                    + 'article/click/?'
                    + new URLSearchParams({link: this.link}),
                    {
                        method: 'POST',
                        headers: {
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Credetials": "true",
                        },
                        credentials: 'include',
                    }
                )
                .then(res => res.json()).then(data => console.log(data))
                .catch(res => console.log(res))

            },
            async love() {

                // if loved already, req to unlove
                const url = this.$store.state.API_BASE_URL 
                    + 'article/love/?' 
                    + new URLSearchParams({link: this.link})

                await fetch(
                    url,
                    {
                        method: 'POST',
                        headers: {
                            "Content-Type": "application/json",
                            "Access-Control-Allow-Credetials": "true",
                        },
                        credentials: 'include',
                    }
                )
                .then(res => res.json()).then(data => {
                    console.log(data)

                })
                .catch(res => console.log(res))
                
                this.loved = !this.loved
            }
        },
    }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    .bi {
        font-size: 2em;
    }

    .bi:hover {
        opacity: 0.3;
    }
</style>
