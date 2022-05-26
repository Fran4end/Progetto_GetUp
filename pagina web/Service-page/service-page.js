// function getPosition() {
//     console.log("on function")
//     var long;
//     var lati;
//     var map = document.querySelector("iframe");
//     fetch("http://192.168.1.77:8081/position")
//         .then(Response => Response.json())
//         .then(data => {
//             long = data.longitudine;
//             lati = data.latitudine;
//             console.log(lati)
//             console.log(long)
//             map.src ="https://www.google.com/maps/embed/v1/search?q=" + lati + "%20" + long + "&key=AIzaSyBwlNQjJ16ua9z5rQ4jnQiF2eMDBpbPq3Q"
//         });
// }

function update() {
    setInterval(a => {getPosition()}, 1000);
    
}

function getPosition() {
    
    fetch("http://192.168.9.30:8081/position")
        .then(Response => Response.json())
        .then(data => {
            long = data.longitudine;
            lati = data.latitudine;
            console.log(lati)
            console.log(long)
            const geojson = {
                'type': 'FeatureCollection',
                'features': [
                    {
                        'type': 'Feature',
                        'geometry': {
                            'type': 'Point',
                            'coordinates': [long, lati]
                        },
                        'properties': {
                            'title': 'demo bus',
                            'description': 'demo bus'
                        }
                    }
                ]
            };
            for (const feature of geojson.features) {
                // create a HTML element for each feature
                const el = document.createElement('div');
                el.className = 'marker';

                // make a marker for each feature and add it to the map
                new mapboxgl.Marker(el)
                    .setLngLat(feature.geometry.coordinates)
                    .setPopup(
                        new mapboxgl.Popup({ offset: 25 }) // add popups
                            .setHTML(
                                `<h3>${feature.properties.title}</h3><p>${feature.properties.description}</p>`
                            )
                    )
                    .addTo(map);
            }

            for (const feature of geojson.features) {
                // create a HTML element for each feature
                const el = document.createElement('div');
                el.className = 'marker';
                // make a marker for each feature and add to the map
                new mapboxgl.Marker(el).setLngLat(feature.geometry.coordinates).addTo(map);
            }
        });

    mapboxgl.accessToken = 'pk.eyJ1IjoiZnJhbjRlbmQiLCJhIjoiY2wzbHdicTZuMDN2bzNqcGpnZHAzbW80dCJ9.or8tRe6iTyOdgO2kYao3yw';
    const map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/light-v10',
        center: [12.3, 45.48],
        zoom: 12
    });
}