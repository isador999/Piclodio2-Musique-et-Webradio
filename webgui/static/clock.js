$(document).ready(function() {
    
    function displayTime() {
		// This gets a "handle" to the clock div in our HTML
		var clockDiv = document.getElementById('clock');
		var clock = clockDiv.innerHTML;
		var datesplited = clock.split(":");
		// convert to date
		var currentTime = new Date(0,0,0,datesplited[0],datesplited[1],datesplited[2]);
		// increment one second
		currentTime.setSeconds(currentTime.getSeconds() + 1);
		var hours = currentTime.getHours();		
		var minutes = currentTime.getMinutes();
		var seconds = currentTime.getSeconds();
		 
		if (seconds == 60){ seconds = 00}
		if(hours < 10){ hours = "0"+hours}
		if(minutes < 10){ minutes = "0"+minutes}
		if(seconds < 10){ seconds = "0"+seconds}
		// set text inside the div
		clockDiv.innerText = hours + ":" + minutes + ":" + seconds;
    }
    
    
    // This runs the displayTime function the first time
	displayTime();
	setInterval(displayTime, 1000);

});
