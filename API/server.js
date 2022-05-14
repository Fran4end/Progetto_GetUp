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

app.get('/?', function(__req, res){
	res.end("ciao")
})
