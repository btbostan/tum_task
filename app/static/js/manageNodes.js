var markers = {};  // Object to hold markers

    document.getElementById('manageNodeForm').addEventListener('submit', function(e) {
        e.preventDefault();  // Prevent the default form submission

        var nodeName = document.getElementById('nodeName').value;
        var latitude = parseFloat(document.getElementById('latitude').value);
        var longitude = parseFloat(document.getElementById('longitude').value);
        var coordKey = `${latitude},${longitude}`; // Create a unique key for the marker

        if (!isNaN(latitude) && !isNaN(longitude)) {
            if (!markers[coordKey]) {  // Check if marker doesn't already exist
                fetch('/add-node', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({name: nodeName, latitude: latitude, longitude: longitude})
                })
                .then(response => response.json())
                .then(data => {
                    if(data.success) {
                        var marker = L.marker([latitude, longitude]).addTo(map);
                        markers[coordKey] = marker;  // Save the marker
                    } else {
                        alert(data.message); // Alert if node already exists or any other server message
                    }
                })
                .catch(err => console.error(err));
            } else {
                alert("Marker already exists at these coordinates");
            }
        } else {
            alert("Invalid coordinates");
        }
    });

    document.getElementById('deleteNode').addEventListener('click', function() {
        var latitude = parseFloat(document.getElementById('latitude').value);
        var longitude = parseFloat(document.getElementById('longitude').value);
        var coordKey = `${latitude},${longitude}`;

        if (!isNaN(latitude) && !isNaN(longitude) && markers[coordKey]) {
            fetch('/delete-node', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({latitude: latitude, longitude: longitude})
            })
            .then(response => response.json())
            .then(data => {
                if(data.success) {
                    map.removeLayer(markers[coordKey]);  // Remove the marker from the map
                    delete markers[coordKey];  // Remove the marker from the object
                    alert("Node deleted successfully");
                } else {
                    alert(data.message); // Alert if node not found or any other server message
                }
            })
            .catch(err => console.error(err));
        } else {
            alert("No marker found at these coordinates");
        }
    });