document.getElementById("captureImageButton").onclick = function() { changeImage() };
document.getElementById("generateCaptionButton").onclick = function() { generateCaption() };

function changeImage() {
	var xhr = new XMLHttpRequest();
	var image_endpoint = "http://10.0.2.15:5000/image";
	xhr.open("GET", image_endpoint);
	xhr.send();
	xhr.onreadystatechange=(e)=>{
		image_url = "../assets/images/6212487_1cca7f3f_1024x1024.jpg";
		if (xhr.responseText == 1) {
			image_url = "../assets/images/COCO_val2014_000000060623.jpg";
		} else if (xhr.responseText == 2) {
			image_url= "../assets/images/COCO_val2014_000000165547.jpg";
		} else if (xhr.responseText == 3) {
			image_url= "../assets/images/COCO_val2014_000000354533.jpg";
		} else if (xhr.responseText == 4) {
			image_url= "../assets/images/COCO_val2014_000000386164.jpg";
		} else if (xhr.responseText == 5) {
			image_url= "../assets/images/COCO_val2014_000000562207.jpg";
		} else if (xhr.responseText == 6) {
			image_url= "../assets/images/COCO_val2014_000000579664.jpg";
		} else if (xhr.responseText == 7) {
			image_url= "../assets/images/CONCEPTUAL_01.jpg";
		} else if (xhr.responseText == 8) {
			image_url= "../assets/images/CONCEPTUAL_02.jpg";
		} else if (xhr.responseText == 9) {
			image_url= "../assets/images/CONCEPTUAL_03.jpg";
		} else if (xhr.responseText == 10) {
			image_url= "../assets/images/CONCEPTUAL_04.jpg";
		} else if (xhr.responseText == 11) {
			image_url= "../assets/images/CONCEPTUAL_05.jpg";
		} else {
			image_url= "../assets/images/CONCEPTUAL_06.jpg";
		}
		document.getElementById("picture").src = image_url;
	}
}

function generateCaption() {
	var xhr = new XMLHttpRequest();
	var image_endpoint = "http://10.0.2.15:5000/clip";
	document.querySelector("#clipResult").innerHTML = "Generating Caption...(can take up to 45 seconds)"
	xhr.open("POST", image_endpoint);
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");
	xhr.send(JSON.stringify({
	    img: document.getElementById("picture").src
	}));
	xhr.onreadystatechange=(e)=>{
		var jsonResponse = JSON.parse(xhr.responseText);
		document.querySelector("#clipResult").innerHTML = jsonResponse["inference"].toUpperCase();
		var msg = new SpeechSynthesisUtterance();
		msg.text = jsonResponse["inference"];
		window.speechSynthesis.speak(msg);
	}
}
