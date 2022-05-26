const express = require('express');
const cors= require('cors');
const {spawn} = require('child_process');

const app = express();
const gps = spawn('python', ['GPS.py']);

const port = 8081;
app.use(cors());

app.listen(port, function(err){
	if(err){
		console.log("errore nello start");
	}else{
		console.log("started");
	}
})

app.get('/position', function(__req, res){
	var latitudine = 45.5;
	var longitudine = 12.3;
	gps.stdout.on("data", (data) => {
		console.log("Py output: " + data);
		coo = data.split(' ');
		latitudine = coo[0];
		longitudine = coo[1];
	})
	var dat = JSON.stringify({'latitudine': latitudine, 'longitudine' : longitudine});
	res.send(dat);

	//Gestisce l'errore dello script python
	gps.stderr.on("data", (data) => {
		console.log("Py error: " + data);
	})	
	res.end();
})
