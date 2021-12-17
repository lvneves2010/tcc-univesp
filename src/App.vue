<template>
  <div id="app">

    <Presentation msg=" Seja Bem Vindo"/>
    <img alt="Hack" src="./assets/hackSM.png">
    <img alt="Willy" src="./assets/willySM.png">
    <img alt="Mumu" src="./assets/mumuSM.png">
    <img alt="Leo" src="./assets/leoSM.png">
    <Presentation msg="Esse é o nosso TCC"/>
  </div>
</template>

<script>
import Presentation from './components/Presentation.vue'

export default {
  name: 'App',
  components: {
    Presentation
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
