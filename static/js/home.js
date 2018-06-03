var chartData = {};
var apiUrl = "http://localhost:8000/get_price_deltas/"
var chart;

$(document).ready(function() {
  getChartDataAndDrawIt()
})

function getChartDataAndDrawIt() {
  $.ajax({
    dataType: "json",
    url: apiUrl,
    success: function(response) {
      chartData = createChartDataFromResponse(response);
      chart = new Chart(document.getElementById("chartJSContainer"), chartData)
    }
  });
}

function clearChartData() {
  chart.data.datasets.forEach((dataset) => {
      dataset.data.pop();
  });
  chart.update();
}

function refreshChart() {
  console.log('refreshing chart')
  clearChartData();
  getChartDataAndDrawIt();
}

setTimeout(function() {
  setInterval(refreshChart(), 15000); // Update every 15 seconds
}, 15000)


function makeRandomHexColor() {
  return "#" + Math.random().toString(16).slice(2, 8);
}

function createChartDataFromResponse(response) {
  var datasets = [];
  var symbols = Object.keys(response);

  symbols.forEach(function(symbol) {
    if (symbol !== 'times') {
      deltas = response[symbol];
      datasets.push({
        label: symbol,
        data: deltas,
        borderColor: makeRandomHexColor(),
        fill:false,
      })
    }
  })

  return {
    type: 'line',
    data: {labels: response.times, datasets: datasets},
    options: {
      title: {
        display: true,
        text: 'Changelly vs Binance Prices  '
      }
    }
  }
}
