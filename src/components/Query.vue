<template>
    <div>
        <button @click="pressed = true">consulta1</button>
        <div v-if="pressed">
            <a>{{info}}
            </a>
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
  data() {
      return {
          pressed: false,
          info: null
      }
  },
  mounted () {
    axios
      .get('https://dadosabertos.camara.leg.br/api/v2/deputados/')
      .then(response => (this.info = response))
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
