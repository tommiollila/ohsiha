function initMap() {

  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 17,
    center: {lat: 61.49911, lng: 23.78712}
  });

    $.get({
      url: 'getcoordinates',
      success: function(data){
        var keys = Object.keys(data);
        for (var i = 0; i < keys.length; i++) {
          loc = data[keys[i]];
          console.log(loc)
          var first_test = {lat: loc.lat, lng: loc.lon};
          var bubble = new google.maps.Circle({
            center: first_test,
            radius: 8,
            strokeColor: loc.stat,
            strokeOpacity: 0.8,
            strokeWeight: 2,
            fillColor: loc.stat,
            fillOpacity: 0.4
          });
          bubble.setMap(map);
        }
      }
    });


  }
