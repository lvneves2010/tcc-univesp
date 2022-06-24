<template>
    <div>
        <div v-if="expanded">
            <p @click="expanded = false">Gastos mensais &nbsp; &nbsp; &nbsp;  <a><img src="../assets/cima.png" alt="" width="10" height="10"></a></p>
        </div>
        <div v-else>
            <p @click="expanded = true">Gastos mensais &nbsp; &nbsp; &nbsp;  <a><img src="../assets/baixo.png" alt="" width="10" height="10"></a></p>
        </div>
        <div v-if="expanded">
            <LineChart v-bind:expenseSet="expenseSet[0]"/>
            <!-- <ul id="example-1">
                <li v-for="expense in expenseDetails" :key="expense"  class="unit">
                     Valor total Mensal - {{ expense.data }}: R${{ expense.valor.toFixed(2) }} <br> 
                </li>
            </ul>
            <p>{{ expenseSet[0] }}</p> -->
            <p>Valor médio mensal: R$ {{ media[0].media.toFixed(2) }}</p>
            <p>Valor Total: R$ {{ total[0].media.toFixed(2) }}</p>
            <p @click="expanded = false">Fechar</p>
        </div>
    </div>
</template>

<script>
import LineChart from './Line.vue'
export default {
  name: 'Expenses',
  components: { LineChart },
  props: {
    expenseDetails: {},
    media: null,
    total: null,
    expenseSet: []
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
