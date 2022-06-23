<template>
    
    <div class="card">
        <img :src="randomPic" class="card-img-top" alt="...">
        <div class="card-body">
            <h5 class="card-title">{{this.title}}</h5>
            <a :href="this.link" target="_blank" class="small">{{this.link}}</a>
            <p class="card-text">{{this.summary}}</p>

            <div class="d-flex justify-content-end">
                <div class="d-flex flex-column align-items-center">
                    <i class="bi bi-hand-thumbs-up-fill text-primary" @click="like"></i>
                    <span>{{this.likeCounter}}</span>
                </div>

                <div class="d-flex flex-column align-items-center ms-4">
                    <i class="bi bi-heart-fill text-danger" @click="love"></i>
                    <span>{{this.loveCounter}}</span>
                </div>
            </div>
            
                    
        </div>
    </div>

</template>

<script>

export default {
    name: 'Article',

    props: {
        title: String,
        link: String,
        summary: String,
        clicked: Number,
        liked: Number
    },

    computed: {
        randomPic() {
            return `https://picsum.photos/seed/` + Math.floor(Math.random() * 100) + `/600/400`
        }
    },

    methods: {
        like() {
            this.likeCounter++
        },

        love() {
            this.loveCounter++
        }
    },

    data() {
        return {
            likeCounter: this.liked,
            loveCounter: this.clicked
        }
    }
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
