<template>
    

    <div class="container">
    
        <h1 v-if="this.topic" class="m-3 display-6">{{this.topic}}</h1>
        <h1 v-else class="m-3 display-6">Welcome, UnionBank and Aboitiz!</h1>
        
        <div class="d-grid gap-5 articles p-3 pb-5" v-if="this.topic">
            <Article
                v-for="article in this.articles"
                :key="article['_id']"
                :id="article['_id']"
                :link="article.link"
                :title="article.title"
                :summary="article.summary"
                :loves="article.loves"
            />
        </div>
    </div>
        
</template>

<script>

    import Article from './Article.vue'
    import axios from 'axios'

    export default {
        name: 'Articles',
        
        props: {
            topic: String
        },

        components: { Article },

        watch: {
            topic(newTopic) {
                axios
                .get('http://localhost:8000/article', {
                    params: {
                        topic: newTopic
                    }
                })
                .then(response => this.articles = response['data'])
            }
        },

        data() {
            return {
                articles: []
            }
        }
    }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
    
    .articles {
        max-height: 70vh;
        overflow-y: scroll;
    }

</style>







