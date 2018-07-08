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
    responsive: true,
    data: {labels: response.times, datasets: datasets},
    options: {
      title: {
        display: true,
        text: 'Changelly vs Binance Prices (%)'
      }
    }
  }
}

$(document).on('click', '#addSMSToNotify', function() {
  var phone_number = $('#smsNumberInput').val();
  var delta_threshold = $('#deltaThresholdInput').val();

  $.ajax({
    url: 'http://localhost:8000/add_sms_notification_number/',
    data: {phone_number, delta_threshold},
    success: function(response) {
      // replace the table html
      $('#table-container').html(response);
    }
  })
})

$(document).on('click', '.remove-number', function() {
  var phoneNum = $(this).data('phone-number');
  $.ajax({
    url: 'http://localhost:8000/remove_number/',
    data: {'pk': phoneNum},
    success: function(response) {
      $('#table-container').html(response);
    }
  })
})

$(document).on('click', '#delete-all-data', function() {
  var dlete = prompt('This will delete everything. Type "Delete" to confirm');
  if (dlete.trim() === "Delete") {
    $.ajax({
      url: 'http://localhost:8000/delete_all_arb_data/',
      success: function(response) {
        // replace the table html
        alert('All arb deltas were deleted');
        refreshChart();
      }
    })
  } else {
    alert('Incorrect phrase entered');
  }
})
