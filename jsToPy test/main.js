// Importia child_proccess, con cui inizializza spawn (di NodeJS) per chiamare un script di python
const { spawn } = require("child_process");

//Usa il comando da console
const child_process = spawn("python", ["conversione.py"]);

//Gestisce l'output di stampa dello script python
child_process.stdout.on("data", (data) => {
    console.log("Py output: " + data);
})

//Gestisce l'errore dello script python
child_process.stderr.on("data", (data) => {
    console.log("Py error: " + data);
})