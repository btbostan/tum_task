var nodes; // nodes data
var links; // links data
var markers = {};  // Object to hold markers
var lines = {}; // Object to hold lines
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
        if (!nodes || !links) return; // Check if nodes and links exist
    
        nodes.forEach(node => {
            if (node.coordinates && node.coordinates.y !== undefined && node.coordinates.x !== undefined) {
                var latitude = parseFloat(node.coordinates.y);
                var longitude = parseFloat(node.coordinates.x);
                var coordKey = `${latitude},${longitude}`;
    
                var marker = L.marker([latitude, longitude])
                    .bindPopup(node.id+ ": "+ node.coordinates.y+ ", "+ node.coordinates.x)
                    .addTo(map);
                markers[coordKey] = marker;
            } else {
                console.error('Invalid node data:', node);
            }
        });
    
        links.forEach(link => {
            // Assuming link.source and link.target are names or IDs of nodes, and you need to find their coordinates
            var sourceNode = nodes.find(node => node.id === link.source);
            var targetNode = nodes.find(node => node.id === link.target);
    
            if (sourceNode && targetNode) {
                var sourceCoordKey = `${parseFloat(sourceNode.coordinates.y)},${parseFloat(sourceNode.coordinates.x)}`;
                var targetCoordKey = `${parseFloat(targetNode.coordinates.y)},${parseFloat(targetNode.coordinates.x)}`;
    
                if (markers[sourceCoordKey] && markers[targetCoordKey]) {
                    var latlngs = [markers[sourceCoordKey].getLatLng(), markers[targetCoordKey].getLatLng()];
                    var polyline = L.polyline(latlngs, { color: 'blue' }).addTo(map);
    
                    var lineKey = link.source + "-" + link.target;

                    lines[lineKey] = polyline;
                }
            }
        });
    }