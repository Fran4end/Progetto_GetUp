function getPosition() {
    var long = 0;
    var lati = 0;
    var map = document.querySelector("iframe");
    fetch("http://192.168.1.77/position")
    .then(res => res.json())
    .then(longitudine, latitudine => {
        long = longitudine;
        lati = latitudine;
    });
    map.src = "https://maps.google.com/maps?q="+ lati + "%20"+ long + "&amp;t=&amp;z=13&amp;ie=UTF8&amp;iwloc=&amp;output=embed"
}

function upDate() {
    setInterval(getPosition(), 500);
}