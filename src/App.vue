<template>
  <Home />
</template>

<script>
import Home from './views/Home.vue'

export default {
  name: 'App',
  components: {
    Home
  }
}
</script>

<style>
 body {
    background-image: url('./assets/bg.jpg');
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-position: center;
  }
</style>
