<template>
    <div>
        <div v-if="expanded">
            <p @click="expanded = false">Proposições próprias &#8679;</p>
        </div>
        <div v-else>
            <p @click="expanded = true">Proposições próprias &#8681;</p>
        </div>
        <div v-if="expanded">
            <p @click="expanded = false">Fechar</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Propositions',
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
          despesas: null,
          expanded: false
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
p {
    cursor: pointer;
}
p:hover {
    color:blue;
}
</style>
