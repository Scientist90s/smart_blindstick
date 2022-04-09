let counter = 0;
if ("webkitSpeechRecognition" in window) {
  let speechRecognition = new webkitSpeechRecognition();
  let final_transcript = "";

  speechRecognition.continuous = true;
  speechRecognition.interimResults = true;
  speechRecognition.lang = document.querySelector("#select_dialect").value;

  speechRecognition.onstart = () => {
    document.querySelector("#status").style.display = "block";
  };
  speechRecognition.onerror = () => {
    document.querySelector("#status").style.display = "none";
    console.log("Speech Recognition Error");
  };
  speechRecognition.onend = () => {
    document.querySelector("#status").style.display = "none";
    console.log("Speech Recognition Ended");
  };

  speechRecognition.onresult = (event) => {
    let interim_transcript = "";

    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        final_transcript += event.results[i][0].transcript;
      } else {
        interim_transcript += event.results[i][0].transcript;
      }
    }
    document.querySelector("#final").innerHTML = final_transcript;
    if (final_transcript !== '' && counter == 0) {
    	counter = 1;
    	var xhr = new XMLHttpRequest();
	xhr.open("POST", "http://10.0.2.15:5000/vilt");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.send(JSON.stringify({
	    que: document.querySelector("#final").innerHTML.concat("?")
	}));
	xhr.onreadystatechange=(e)=>{
		var jsonResponse = JSON.parse(xhr.responseText);
		document.querySelector("#result").innerHTML = jsonResponse["ans"].toUpperCase();
		var msg = new SpeechSynthesisUtterance();
		msg.text = jsonResponse["ans"];
		window.speechSynthesis.speak(msg);
		final_transcript = "";
		counter = 0;
	}
    }
    document.querySelector("#interim").innerHTML = interim_transcript;
  };

  document.querySelector("#start").onclick = () => {
    speechRecognition.start();
  };
  document.querySelector("#stop").onclick = () => {
    speechRecognition.stop();

  };
} else {
  console.log("Speech Recognition Not Available. Make sure to use Chrome!");
}
