const express = require('express');
const cors= require('cors');
const fs = require('fs');

const app = express();

const port = 8081;
app.use(cors());

app.listen(port, function(err){
	if(err){
		console.log("errore nello start");
	}else{
		console.log("started");
	}
})

app.get('/?', function(__req, res){
	var file = fs.readFileSync('/home/pi/Desktop/Progetto_GetUp/pySQLite/info.json');
	var data = JSON.parse(file);
	res.end(data)
})
