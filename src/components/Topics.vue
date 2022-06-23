<template>
  <div class="d-grid gap-2">
    
    <button class="btn btn-warning mt-4 shadow" type="button" data-bs-toggle="collapse" data-bs-target="#topics" aria-expanded="false" aria-controls="topics">
      Topics
    </button>

    <div class="collapse" id="topics">
      <ul class="list-group">
        <li 
          class="list-group-item" 
          v-for="(topic, key, index) in topics"
          :key="index"
          @click="selectTopic(topic)"
          >
          {{topic}}
        </li>
      </ul>
    </div>

  </div>

</template>

<script>

  export default {
      name: 'Topics',
      
      methods: {
        async selectTopic(topic) {
          this.$emit('selectTopic', topic)
        }
      },

      data() {
        return {
          topics: ['Machine Learning and AI Ethics', 'Finance and Business', 'Power and Energy', 'Blockchain', 'Space News Research']
        }
      }
  }

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>

