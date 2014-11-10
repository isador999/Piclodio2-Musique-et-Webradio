$(function() {
  $("#message").hide();
});



function dayClicked(dayButton){
    var btn = document.getElementById(dayButton); 
    if (btn.className== "btn btn-default"){
        btn.className= "btn btn-primary";
    }else{
        btn.className= "btn btn-default";
    }
    
}


function modeClicked(modeButton){
    var btn = document.getElementById(modeButton);
    if (btn.className== "btn btn-default"){
        btn.className= "btn btn-primary";
    }else{
        btn.className= "btn btn-default";
    }

}



function goAddAlarmClock(){
    // get all selection
    var label   = document.getElementById("label").value;
    var hour    = document.getElementById("hour").value;
    var minute  = document.getElementById("minute").value;
    var snooze  = document.getElementById("snooze").value;
    var webradio= document.getElementById("webradio").value;
    var dayofweek="";
    var first = 0; // boolean to detect the first insert
    var table = ["suButton", "moButton","tuButton","weButton","thButton","frButton","saButton"];
    for (var i=0;i<table.length;i++){
        var dayButton = document.getElementById(table[i]);
        if(dayButton.className == "btn btn-primary"){
            if (first == 0){ // if it's the fisrt time we add a number no float
                dayofweek+= i.toString();
                first =1;   // we found one
            }else{
                dayofweek+= ","+i.toString();
            }
        }
    }
    

//    var mode="";
//    var choice = ["music", "radio"];
//    var mButton = "musicButton";
//    var rButton = "radioButton";
    
    var modeMusic = document.getElementById('music');
    var modeRadio = document.getElementById('radio');
    if(modeRadio.className == "btn btn-primary"){
        if(modeMusic.className == "btn btn-default"){
            mode= "radio";
       } else{
            mode= "music";
        }
    }else{
    	mode= "music";
    }

    

    // send all of that shit to the server
    $.ajax({
        type: "POST",               
        url: "addalarmclock",
        dataType: "json",
        traditional: true,
        data: {label: label,hour: hour,minute:minute, snooze:snooze, webradio:webradio,dayofweek:dayofweek,mode:mode,},
        success: function(data){ 
            if (data["HTTPRESPONSE"]=="error"){
                $("#message").html("<strong>Oh snap! </strong> Change a few things up and try submitting again.");
                // show
                $("#message").show();
                $("#message").alert();
                // hide after 3 seconds
                var t = setTimeout("$(\"#message\").hide() ;",3000);
            }else{
                var url = data["HTTPRESPONSE"];
                window.location.replace(url);
            }
        }    
    });
    
    
}
