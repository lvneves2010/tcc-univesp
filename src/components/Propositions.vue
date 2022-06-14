<template>
    <div>
        <div v-if="expanded">
            <p @click="expanded = false">Proposições próprias &nbsp; &nbsp; &nbsp;  <a><img src="../assets/cima.png" alt="" width="10" height="10"></a></p>
        </div>
        <div v-else>
            <p @click="expanded = true">Proposições próprias &nbsp; &nbsp; &nbsp;  <a><img src="../assets/baixo.png" alt="" width="10" height="10"></a></p>
        </div>
        <div v-if="expanded">
            <ul>
                <li id="individual_prop" v-for="proposition in propositions" :key="proposition"  class="unit">
                    {{ proposition.ano }} <br> {{ proposition.ementa }} <br> {{ proposition.tema }}
                </li>
            </ul>
            <p @click="expanded = false">Fechar</p>
        </div>
    </div>
</template>

<script>
export default {
  name: 'Propositions',
  props: {
    propositions: {}
  },
  data() {
      return {
          expanded: false
      }
  },
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
