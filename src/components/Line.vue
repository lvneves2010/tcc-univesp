<template>
  <LineChartGenerator
    :chart-options="chartOptions"
    :chart-data="chartData"
    :chart-id="chartId"
    :dataset-id-key="datasetIdKey"
    :plugins="plugins"
    :css-classes="cssClasses"
    :styles="styles"
    :width="width"
    :height="height"
  />
</template>

<script>
import { Line as LineChartGenerator } from 'vue-chartjs/legacy'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement
} from 'chart.js'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  LinearScale,
  CategoryScale,
  PointElement
)

export default {
  name: 'LineChart',
  components: { LineChartGenerator },
  props: {
    chartId: {
      type: String,
      default: 'line-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
    width: {
      default: 400
    },
    height: {
      default: 400
    },
    cssClasses: {
      default: '',
      type: String
    },
    styles: {
      type: Object,
      default: () => {}
    },
    plugins: {
      type: Array,
      default: () => []
    },
    expenseSet: []
  },
  data() {
    return {
      chartData: {
        labels: [ 'Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
        datasets: [ {
            label: 'gastos mensais',
            backgroundColor: '#FFFFFF',
            borderColor:'#EDB64C', 
            data: this.expenseSet }
        ]
      },
      chartOptions: {
        plugins: {
            legend: {
                display: false
            },
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
              y: {
                  grid: {
                    color: '#685D6E'
                  },
                  ticks: {
                      color: '#FFFFFF'
                    }
              },
              x: {
                    grid: {
                      color: '#685D6E'
                    },
                          ticks: {
                      color: '#FFFFFF'
                    }
              }
        }
      }
    }
  }
}
</script>