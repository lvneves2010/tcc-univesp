<template>
    <div>
        <button @click="pressed = true">inicio</button>
        <div v-if="pressed">
          <ul id="example-1">
            <li v-for="info in infos" :key="info.id">
              <button @click="selected(info.id)">
                {{ info.nome }} - {{ info.siglaPartido }}
              </button>
            </li>
          </ul>
        </div>
        <div v-if="choosen">
          <a href="">{{ details }}</a>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Query',
  props: {
    msg: String
  },
  methods: {
    selected(id) {
      this.pressed = false;
      axios.get(`https://dadosabertos.camara.leg.br/api/v2/deputados/${id}`).then(res => (
        this.details = res,
        this.choosen = true
      ))

      console.log("Olá");
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
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
