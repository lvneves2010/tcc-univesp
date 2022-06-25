<template>
  <div id="app">
    <div v-if="logged">
      <button @click="logged = false">Sair</button>
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
  color: white;
  margin-top: 60px;
  background-color: #3c2747;
}

body {
  background-color: #3c2747;
}

button {
  color: #ff1d5e;
  background-color: #3c2747;
  cursor: pointer;
}

</style>
