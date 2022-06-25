<template>
    <div v-if="newInfo !== null">

        <!-- <button @click="pressed = true; choosen = false">inicio</button> -->
        <div v-if="pressed">

          <div style="display: inline">
                  <input v-model="text_to_search" id='buscador' placeholder="Nome do deputado" />
                  <button @click="search(text_to_search, newInfo)">Buscar</button>
                  <button @click="clearSearch()">Limpar</button>
          </div>

          <ul id="example-1">
            <li v-for="info in filtered_info" :key="info.id" @click="newSelected(info.id)" class="unit">
                <img :src="info.url_foto" alt="" width="40" height="50">
              <button @click="newSelected(info.id)">
                {{ info.nome }} ( {{ info.partido }} / {{ info.partido_uf}} ) <br>
                Gastos ultimo Mês: R$ {{ info.despesa_mes.toFixed(2) }}
              </button>
            </li>
          </ul>

        </div>

        <button v-if="choosen" @click="pressed = true; choosen = false; expenseSet = []">voltar</button>
        
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
                v-bind:expenseSet="expenseSet"
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
    <div v-else>
        <div class="half-circle-spinner center">
          <div class="circle circle-1"></div>
          <div class="circle circle-2"></div>
      </div>
    </div>

</template>

<script>
import fuzzysort from 'fuzzysort'
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
      axios.get(`https://tccunivesp.iaguaru.com.br/deputado?id=${id}`).then(res => (
        this.details = res.data.dados[0],
        this.choosen = true
      ))
      axios.get(`https://tccunivesp.iaguaru.com.br/deputado/${id}/despesas/`).then(res => (
        this.expenseDetails = res.data.dados.despesas,
        this.expenseSet.push((this.expenseDetails.map(e => parseInt(e.valor.toFixed(2))))),
        this.media = res.data.dados.media_despesas,
        this.total = res.data.dados.total_despesas,
        this.choosen = true
      ))
      axios.get(`https://tccunivesp.iaguaru.com.br/deputado/${id}/proposicoes/`).then(res => (
        this.propositions = res.data.dados,
        this.choosen = true
      ))
      axios.get(`https://tccunivesp.iaguaru.com.br/deputado/${id}/votacoes/`).then(res => (
        this.votes = res.data.dados,
        this.choosen = true
      ))
    },

    search(text, array){
      var results = fuzzysort.go(text, array, {key:'nome'})
      this.filtered_info = results.map(function(item) {
                        return item.obj;
                      });
    },

    clearSearch(){
      console.log('limpando')
      this.filtered_info = this.newInfo;
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
          oldInfo: null,
          filtered_info: null,
          text_to_search: null,
          expenseDetails: null,
          votes: null,
          propositions: null,
          media: null,
          total: null,
          expenseSet: []
      }
  },
  mounted () {
    axios
      .get('https://tccunivesp.iaguaru.com.br/deputado?limite=513')
      .then(response => (this.newInfo = response.data.dados, this.filtered_info = response.data.dados))
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
  color: #ff1d5e;
  background-color: #3c2747;
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
.center {
  margin: auto;
  padding: 10px;
}
.half-circle-spinner, .half-circle-spinner * {
      box-sizing: border-box;
    }

    .half-circle-spinner {
      width: 60px;
      height: 60px;
      border-radius: 100%;
      position: relative;
    }

    .half-circle-spinner .circle {
      content: "";
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 100%;
      border: calc(60px / 10) solid transparent;
    }

    .half-circle-spinner .circle.circle-1 {
      border-top-color: #ff1d5e;
      animation: half-circle-spinner-animation 1s infinite;
    }

    .half-circle-spinner .circle.circle-2 {
      border-bottom-color: #ff1d5e;
      animation: half-circle-spinner-animation 1s infinite alternate;
    }

    @keyframes half-circle-spinner-animation {
      0% {
        transform: rotate(0deg);

      }
      100%{
        transform: rotate(360deg);
      }
    }

</style>
