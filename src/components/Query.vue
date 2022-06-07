<template>
    <div>
        <!-- <button @click="pressed = true; choosen = false">inicio</button> -->
        <div v-if="pressed">
          <ul id="example-1">
            <li v-for="info in infos" :key="info.id" @click="selected(info.id)" class="unit">
                <img :src="info.urlFoto" alt="" width="40" height="50">
              <button @click="selected(info.id)">
                {{ info.nome }} ( {{ info.siglaPartido }} / {{ info.siglaUf}} ) 
              </button>
            </li>
          </ul>
        </div>
        <button v-if="choosen" @click="pressed = true; choosen = false">voltar</button>
        <div v-if="choosen">
          <div  style="display: inline-flex">
            <div>
              <img :src="details.ultimoStatus.urlFoto" alt="" width="64" height="80">
            </div>
            <div>
                <p >{{ details.nomeCivil }}</p>
                <p>{{ details.ultimoStatus.siglaPartido }} / {{ details.ultimoStatus.siglaUf}} - {{ details.ultimoStatus.email }}</p>
            </div>
          </div>
          <ul  style="display: grid" >
            <li class="tabs">
              <Expenses />
            </li>
            <li class="tabs">
              <Votes />
            </li>
            <li class="tabs">
              <Propositions />
            </li>
          </ul>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import Expenses from './Expenses.vue'
import Votes from './Votes.vue'
import Propositions from './Propositions.vue'
export default {
  name: 'Query',
  components: {
    Expenses,
    Votes,
    Propositions
  },
  props: {
    msg: String
  },
  methods: {
    selected(id) {
      this.pressed = false;
      axios.get(`https://dadosabertos.camara.leg.br/api/v2/deputados/${id}`).then(res => (
        this.details = res.data.dados,
        this.choosen = true
      ));
      axios.get(`https://dadosabertos.camara.leg.br/api/v2/deputados/${id}/despesas`).then(res => (
        this.despesas = res.data.dados,
        this.choosen = true
      ));
    }
  },
  data() {
      return {
          pressed: true,
          choosen: false,
          infos: null,
          details: null,
          despesas: null
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
button {
  color: #000000;
  background-color:#ffffff;
  cursor: pointer;
}
.unit {
  cursor: pointer;
}
img {
  border: 0.5px solid #b0afaf;
  border-radius: 50%;
}
.tabs {
  border: 0.5px solid #b0afaf;
  margin: 1rem;
}
</style>
