$(document).ready(function() {
    
    function displayTime() {
		// This gets a "handle" to the clock div in our HTML
		var clockDiv = document.getElementById('clock');
		var clock = clockDiv.innerHTML;
		var datesplited = clock.split(":");
		// convert to date
		var currentTime = new Date(0,0,0,datesplited[0],datesplited[1],datesplited[2]);
		var hours = currentTime.getHours();
		var minutes = currentTime.getMinutes();
		var seconds = currentTime.getSeconds();
		seconds +=1;
		// set text inside the div
		clockDiv.innerText = hours + ":" + minutes + ":" + seconds;
    }
    
    
    // This runs the displayTime function the first time
	displayTime();
	setInterval(displayTime, 1000);

});
