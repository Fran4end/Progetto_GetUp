const express = require('express');
const cors= require('cors');
const fs = require('fs');
const {spawn} = require('child_process');

const app = express();
gps = spawn('python', ['GPS.py']);

const port = 8069;
app.use(cors());

app.listen(port, function(err){
	if(err){
		console.log("errore nello start");
	}else{
		console.log("started");
	}
})

app.get('/position', function(__req, res){
	gps.stdout.on('data', (data) => {console.log(data)});
	var latitudine = 45.5;
	var longitudine = 12.3;
	const data = fs.readFileSync('./info.json', 'utf8');
	coo = String(data).replace('\n', '').split(' ');
	latitudine = coo[0];
	longitudine = coo[1];
	dat = JSON.stringify({'latitudine': latitudine, 'longitudine' : longitudine});
	res.send(dat);
	res.end();
})
