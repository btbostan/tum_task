var lines = {}; // Global varible to store lines
        var map = L.map('map').setView([51.1657, 10.4515], 6); // Center on Germany
    
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);
    