<template>
    

    <div class="container">
    
        <h1 v-if="this.topic" class="m-3 display-6">{{this.topic}}</h1>
        <div v-else class="m-3">
            <h5>Welcome UnionBank and Aboitiz to your One-stop Daily News-letter app powered by AI</h5>
            <p class="lead">
                The articles are recommended just for you based on your previous interest!
                <br>
                Stop by here, to keep up with changes in your industry and evolve with change!
            </p>
        </div>
        
        <div class="d-grid gap-5 articles p-3 pb-5" v-if="this.topic">
            <Article
                v-for="article in this.articles"
                :key="article['link']"
                :id="article['link']"
                :link="article.link"
                :title="article.title"
                :summary="article.summary"
                :clickCounts="article.total_clicks"
                :isLoved="article.loved"
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
            async topic(newTopic) {
                await axios.get(
                    this.$store.state.API_BASE_URL + 'article/recommendations',
                    {
                        params: { topic: newTopic},
                        withCredentials: true,
                    }
                ).then( res => {
                        this.articles = res.data
                    }
                ).catch(res => console.log(res))
                // await fetch(
                //     this.$store.state.API_BASE_URL + 'article?' + new URLSearchParams(
                //         {
                //             topic: newTopic
                //         }
                //     ),
                //     {
                //         method: 'GET',
                //         headers: {
                //             "Content-Type": "application/json",
                //             "Access-Control-Allow-Credetials": "true",
                //         },
                //         credentials: 'include',
                //         // mode: 'no-cors'
                //     }
                // )    
                // .then(res => {
                //     res.json()
                // }).then(data => {
                //     this.articles = data
                // })
                // .catch(res => {
                //     console.log(res)
                // })
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







