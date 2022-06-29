<template>
  <div class="container p-5">
    <div class="row">
      <div class="col">
        <h1 class="display-2 text-center my-5 fw-bolder">Intelligent Newsletter</h1>
      </div>
    </div>
    <div class="row">
      <div class="col-3">
        <div class="d-flex flex-column justify-content-between">
          <Topics @select-topic="selectTopic"/>
          <div class="card text-white bg-secondary mt-5">
            <div class="card-body shadow">
              <p>Welcome to UnionBank and Aboitiz newsletter powered by AI.</p>
              
              <p>
                Press the <b>Topics</b> button to select the topics you want to read.
              </p>

              <p>
                Did you like the article recommended? Do press the <i class="bi bi-heart-fill text-danger"></i> to let us know.
              </p>

            </div>
          </div>
        </div>
      </div>
      <div class="col-9">
        <Articles :topic="this.topic" />
      </div>
    </div>
  </div>

</template>

<script>

  import Articles from '../components/Articles.vue'
  import Topics from '../components/Topics.vue'
  
  export default {
    name: 'Home',

    components: {
      Articles,
      Topics
    },
    
    methods: {
      async selectTopic(topic) {
        this.topic = topic
      }
    },

    data() {
      return {
        topic: ""
      }
    }
  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  
</style>
