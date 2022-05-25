const express = require('express');
const cors= require('cors');

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

app.get('/position', function(__req, res){
	var latitudine = 1;
	var longitudine = 1;
	var data = JSON.stringify({'latitudine': latitudine, 'longitudine' : longitudine});
	res.send(data);
	res.end();
})
