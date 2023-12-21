var nodes; // nodes data
var links; // links data

// Fetch and process nodes from JSON file
fetch('/get-network-data') // Assuming you still have this endpoint for nodes
    .then(response => response.json())
    .then(data => {
        nodes = data;
        processNodesAndLinks();
    });

// Fetch and process links
fetch('/get-link-data')
    .then(response => response.json())
    .then(data => {
        links = data;
        processNodesAndLinks();
    });

function processNodesAndLinks() {
    if (!nodes || !links) return; // Check if they are exist

    var nodeDict = {};
    nodes.forEach(node => {
        var marker = L.marker([parseFloat(node.coordinates.y), parseFloat(node.coordinates.x)])
            .bindPopup(node.id)
            .addTo(map);
        nodeDict[node.id] = marker.getLatLng();
    });

    links.forEach(link => {
        if (nodeDict[link.source] && nodeDict[link.target]) {
            var latlngs = [nodeDict[link.source], nodeDict[link.target]];
            var polyline = L.polyline(latlngs, { color: 'blue' }).addTo(map);
            
        // Store the line reference
        var lineKey = link.source + "-" + link.target;
        lines[lineKey] = polyline;
            
        }
    });
}