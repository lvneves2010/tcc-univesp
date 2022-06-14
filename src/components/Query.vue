<template>
    <div>
        <!-- <button @click="pressed = true; choosen = false">inicio</button> -->
        <div v-if="pressed">
          <ul id="example-1">
            <li v-for="info in newInfo" :key="info.id" @click="newSelected(info.id)" class="unit">
                <img :src="info.url_foto" alt="" width="40" height="50">
              <button @click="newSelected(info.id)">
                {{ info.nome }} ( {{ info.partido }} / {{ info.partido_uf}} ) <br>
                Gastos ultimo Mês: R$ {{ info.despesa_mes }}
              </button>
            </li>
          </ul>
        </div>
        <button v-if="choosen" @click="pressed = true; choosen = false">voltar</button>
        <div v-if="choosen">
          <div  style="display: inline-flex">
            <div>
              <img :src="details.url_foto" alt="" width="64" height="80">
            </div>
            <div>
                <p >{{ details.nome }}</p>
                <p>{{ details.partido }} / {{ details.partido_uf}} - {{ details.email }}</p>
            </div>
          </div>
          <ul  style="display: grid" >
            <li class="tabs">
              <Expenses 
                v-bind:expenseDetails="expenseDetails"
                v-bind:media="media"
                v-bind:total="total"/>
            </li>
            <li class="tabs">
              <Votes v-bind:votes="votes"/>
            </li>
            <li class="tabs">
              <Propositions v-bind:propositions="propositions"/>
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
    newSelected(id) {
      this.pressed = false;
      axios.get(`http://35.237.79.225/deputado?id=${id}`).then(res => (
        this.details = res.data.dados[0],
        this.choosen = true
      ))
      axios.get(`http://35.237.79.225/deputado/${id}/despesas/`).then(res => (
        this.expenseDetails = res.data.dados.despesas,
        this.media = res.data.dados.media_despesas,
        this.total = res.data.dados.total_despesas,
        this.choosen = true
      ))
      axios.get(`http://35.237.79.225/deputado/${id}/proposicoes/`).then(res => (
        this.propositions = res.data.dados,
        this.choosen = true
      ))
      axios.get(`http://35.237.79.225/deputado/${id}/votacoes/`).then(res => (
        this.votes = res.data.dados,
        this.choosen = true
      ))
    }
  },
  data() {
      return {
          pressed: true,
          choosen: false,
          infos: null,
          details: null,
          despesas: null,
          newInfo: null,
          expenseDetails: null,
          votes: null,
          propositions: null,
          media: null,
          total: null
      }
  },
  mounted () {
    axios
      .get('http://35.237.79.225/deputado?limite=200')
      .then(response => (this.newInfo = response.data.dados))
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
