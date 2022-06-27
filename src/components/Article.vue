<template>
    
    <div class="card shadow border-0">
        <img :src="randomPic" class="card-img-top" alt="...">
        <div class="card-body">
            <h5 class="card-title">{{this.title}}</h5>
            <a :href="this.link" target="_blank" class="small text-muted" @click="linkClick">Go to the main article</a>
            <p class="card-text">{{this.summary}}</p>

            <div class="d-flex justify-content-end">
                <div class="d-flex flex-column align-items-center">
                    <i class="bi bi-heart-fill text-danger" @click="love"></i>
                    <span>{{this.loveCount}}</span>
                </div>
            </div>
            
                    
        </div>
    </div>

</template>

<script>
    import axios from 'axios'

    export default {
        name: 'Article',
        
        data() {
            return {
                loveCount: 0
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
            linkClick() {
                axios
                .patch(`http://articles-recommender.azurewebsites.net/api/clicks/${this.id}`)
            },
            love() {
                axios
                .patch(`http://articles-recommender.azurewebsites.net/api/loves/${this.id}`)
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
