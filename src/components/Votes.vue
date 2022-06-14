<template>
    <div>
        <div v-if="expanded">
            <p @click="expanded = false">Votações &nbsp; &nbsp; &nbsp;  <a><img src="../assets/cima.png" alt="" width="10" height="10"></a></p>
        </div>
        <div v-else>
            <p @click="expanded = true">Votações &nbsp; &nbsp; &nbsp;  <a><img src="../assets/baixo.png" alt="" width="10" height="10"></a></p>
        </div>
        <div v-if="expanded">
            <ul id="example-1">
                <li id="individual_prop" v-for="vote in votes" :key="vote"  class="unit">
                     Tema: {{ vote.tema }} <br> Descrição: {{ vote.descricao }} <br><p v-if="vote.voto==0">Votou: Não</p> <p v-if="vote.voto==1">Votou: Sim</p> <br>
                </li>
            </ul>
            <p @click="expanded = false">Fechar</p>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Votes',
  props: {
    votes: {}
  },
  data() {
      return {
          expanded: false
      }
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
ul {
  list-style-type: none;
  padding: 0;
}
#individual_prop {
  border: 0.5px solid #b0afaf;
  margin: 1rem;
}
</style>
