var map = L.map('map').setView([51.505, -0.09], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

map.on('click', function onMapClick(e) {
    $.ajax({
        url: '/get_country_by_coords',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({lat: e.latlng.lat, lon: e.latlng.lng}),
        success: function (response) {
            var countryInfo = response.results.bindings[0];
            var sidebarContent = 'Country: ' + countryInfo.country.value + '<br>' +
                                 'Capital: ' + countryInfo.capital.value + '<br>' +
                                 'Population: ' + countryInfo.populationTotal.value + '<br>' +
                                 'Abstract: ' + countryInfo.abstract.value;
            $('#sidebar').html(sidebarContent);
        },
        error: function (xhr, status, error) {
            console.error(error);
        }
    });
});
