function getline() {
    fetch("http://192.168.4.26:8081/")
        .then(response => console.log(response))
}