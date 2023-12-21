document.getElementById('addLink').addEventListener('click', function() {
    var sourceNodeName = document.getElementById('sourceNode').value;
    var targetNodeName = document.getElementById('targetNode').value;

    fetch('/get-link-coordinates', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({source: sourceNodeName, target: targetNodeName})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {

            var sourceCoords = data.source;
            var targetCoords = data.target;
            var latlngs = [ [sourceCoords.latitude, sourceCoords.longitude], [targetCoords.latitude, targetCoords.longitude] ];
            var polyline = L.polyline(latlngs, { color: 'blue' }).addTo(map);

            // Optionally store the line for future reference
            var lineKey = sourceNodeName + "-" + targetNodeName;
            lines[lineKey] = polyline;
            alert("Link added successfully");
        } else {
            alert(data.message); // Alert if nodes not found or other message
        }
    })
    .catch(err => console.error(err));
});

//Deleting Link

document.getElementById('deleteLink').addEventListener('click', function() {
    var sourceNode = document.getElementById('sourceNode').value;
    var targetNode = document.getElementById('targetNode').value;
    var lineKey = sourceNode + "-" + targetNode;
    fetch('/delete-link', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({source: sourceNode, target: targetNode})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
                // Use the 'lines' object to find and remove the line
            if (lines[lineKey]) {
                map.removeLayer(lines[lineKey]);  // Remove the line from the map
                delete lines[lineKey];  // Remove the line reference from the 'lines' object
                alert("Link deleted successfully");
            } else {
                alert("No visual link found on the map.");
        }
        }
    })
    .catch(err => console.error(err));
});
