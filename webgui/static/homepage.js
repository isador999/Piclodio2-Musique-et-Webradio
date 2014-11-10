

function controlRadioClicked(buttonClicked){
    //--------------------------
    // invert color of buttons
    //--------------------------
    if (buttonClicked == "play"){
        var btn = document.getElementById('play'); 
        btn.className= "btn btn-primary btn-lg"; 
        var btn = document.getElementById('stop'); 
        btn.className= "btn btn-default btn-lg";
    }else{
        var btn = document.getElementById('stop'); 
        btn.className= "btn btn-primary btn-lg"; 
        var btn = document.getElementById('play'); 
        btn.className= "btn btn-default btn-lg";
    }
    
    // call controler
    
}