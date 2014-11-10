$(function() {
  $("#message").hide();
});


function saveTime(){
    // get all selection
    var hour    = document.getElementById("setHour").value;
    var minute  = document.getElementById("setMinute").value;


    // send all of that shit to the server
    $.ajax({
        type: "POST",               
        url: "timeset",
        dataType: "json",
        traditional: true,
        data: {hour: hour,minute:minute,},
        success: function(data){ 
            var url = data["HTTPRESPONSE"];
            window.location.replace(url);
        }    
    });
    
    
}
