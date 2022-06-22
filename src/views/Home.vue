<template>

  <div class="container p-5">
    <div class="row">
      <div class="col-3">
        <Topics @select-topic="selectTopic"/>
      </div>
      <div class="col-9">
        <Articles/>
      </div>
    </div>
  </div>

</template>

<script>

  import Articles from '../components/Articles.vue'
  import Topics from '../components/Topics.vue'
  
  export default {
    name: 'Home',

    methods: {
      async selectTopic(topic) {
        this.topic = topic
      }
    },

    components: {
      Articles,
      Topics
    },

    data() {
      return {
        topic: false
      }
    }
  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
