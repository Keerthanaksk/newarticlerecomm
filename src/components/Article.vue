<template>
    
    <div class="card shadow border-0">
        <!-- <img :src="randomPic" class="card-img-top"> -->
            <h5 class="card-header">{{this.title}}</h5>
        <div class="card-body">
            <div class="d-flex">
                
                <div class="d-flex flex-column align-items-center align-self-center">
                    <i class="bi bi-heart-fill text-danger" @click="love"></i>
                    <span>{{this.loveCount}}</span>
                </div>
                <div class="ms-4">
                    <p class="card-text">{{this.summary}}</p>
                    <a :href="this.link" target="_blank" class="small text-muted align-self-end" @click="linkClick">Read more</a>
                </div>
            </div>
                    
        </div>
    </div>

</template>

<script>
// <div class="d-flex justify-content-end">
//                 <div class="d-flex flex-column align-items-center">
//                     <i class="bi bi-heart-fill text-danger" @click="love"></i>
//                     <span>{{this.loveCount}}</span>
//                 </div>
//             </div>
    import axios from 'axios'

    export default {
        name: 'Article',
        
        data() {
            return {
                loveCount: 0,
                test: ''
            }
        },

        props: {
            id: String,
            title: String,
            link: String,
            summary: String,
            loves: Number
        },

        created() {
            this.loveCount = this.loves
            
        },

        computed: {
            randomPic() {
                return `https://picsum.photos/seed/` + Math.floor(Math.random() * 100) + `/600/400`
            }
        },

        methods: {
            async linkClick() {
                axios
                .patch(`https://articles-recommender.azurewebsites.net/api/clicks/${this.id}`)
            },
            async love() {
                axios
                .patch(`https://articles-recommender.azurewebsites.net/api/loves/${this.id}`)
                .then(response => this.loveCount = response['data']['loves'])
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
