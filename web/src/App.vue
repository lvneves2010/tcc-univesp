<template>
  <div id="app">
    <div v-if="logged">
      <a href="" @click="logged = false">Sair</a>
    </div>

    <Presentation msg=" APP UNIVESP "/>
    <div v-if="logged">
      <Query />
    </div>
    <div v-else>
      <LoginScreen v-on:loggei="loggar" />
    </div>
  </div>
</template>

<script>
import Presentation from './components/Presentation.vue'
import Query from './components/Query.vue'
import LoginScreen from './components/LoginScreen.vue'

export default {
  name: 'App',
  components: {
    Presentation,
    Query,
    LoginScreen
  },
  data() {
      return {
          logged: false
      }
  },
  methods: {
    loggar() {
      this.logged = true; 
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
