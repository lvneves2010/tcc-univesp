<template>
    <div class="root">
        <div style="display: inline">
            <input placeholder="Digite seu email" />
            <button @click="$emit('loggei')">entrar</button>
        </div>

        <a @click="$emit('loggei')">Pular e entrar anonimo</a>
    </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Query',
  methods: {
    selected(id) {
      this.pressed = false;
      axios.get(`https://dadosabertos.camara.leg.br/api/v2/deputados/${id}`).then(res => (
        this.details = res.data.dados,
        this.choosen = true
      ))
    }
  },
  data() {
      return {
          pressed: false,
          choosen: false,
          infos: null,
          details: null
      }
  },
  mounted () {
    axios
      .get('https://dadosabertos.camara.leg.br/api/v2/deputados/')
      .then(response => (this.infos = response.data.dados))
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
a {
    margin: 3rem;
    cursor: pointer;
    text-decoration: underline;
}
a:hover {
    color: #2b2be4;
}
input {
    min-width: 15rem;
}
button {
    color: #ffffff;
    background-color: #2b2be4;
    cursor: pointer;
}
.root {
    display:inline-grid;
}
</style>
