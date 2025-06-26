/* globals Chart:false */

(() => {
  'use strict'

  // Graphs
  const ctx = document.getElementById('myChart')
  // eslint-disable-next-line no-unused-vars
  const myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: {{axis_x | tojson}},
      datasets: [
        // y축 데이터 1개 dict로 구성
        {
          // data y축 데이터
        data: {{axis_y | tojson}},
        lineTension: 0,
        backgroundColor: 'transparent',
        borderColor: '#007bff',
        borderWidth: 4,
        pointBackgroundColor: '#007bff'
        }
      ]
    },
    options: {
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          boxPadding: 3
        }
      }
    }
  })
})()
