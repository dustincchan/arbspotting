
$(document).ready(function() {
  getBizData();
})

function getBizData() {
  $.ajax({
    dataType: "jsonp",
    url: "http://localhost:8000/",
    success: function(response) {
      console.log(response);
    },
    error: function (xhr, ajaxOptions, thrownError) {
      alert(xhr.status);
      alert(thrownError);
    }
  });
}
