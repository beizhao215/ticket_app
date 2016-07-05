var mymap = L.map('mapid').setView([43.6532, -79.3832], 13);
L.tileLayer('https://api.tiles.mapbox.com/v4/mapboxid/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'ticketapp',
    accessToken: 'my_token'
}).addTo(mymap);



mymap.on('click', onMapClick);
var lat
var lng
var currentdate = new Date();
var popup = L.popup();

function onMapClick(e) {
    var latlon = e.latlng;
    lat = latlon.lat;
    lng = latlon.lng;
    currenttime = currentdate.getHours() + ":" + currentdate.getMinutes()
    var a = $("#data").text(lat);
    $('p[name=a]').text("Latitude: "+lat);
    $('p[name=b]').text("Longitude: "+lng);
    $('p[name=c]').text("Time: "+currenttime);
    popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(mymap);

}





mymap.on('click', onMapClick);


$(function() {
    var submit_form = function(e) {
      $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
        a: lat,
        b: lng
      }, function(data) {
//        $('#result').text(data.result);
        $('#result1').text(data.result[0]);

        $('#result2').text(data.result[1]);
        $('#result3').text(data.result[3]);
        $('#result4').text(data.result[4]);
        $('#result5').text(data.result[6]);
        $('#result6').text(data.result[7]);


        $('input[name=a]').focus().select();
      });
      return false;
    };
    $('a#calculate').bind('click', submit_form);
    $('input[type=text]').bind('keydown', function(e) {
      if (e.keyCode == 13) {
        submit_form(e);
      }
    });
    $('input[name=a]').focus();
  });
