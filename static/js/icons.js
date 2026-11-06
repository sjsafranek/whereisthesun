
const Icons = {
    // Define a custom sun divIcon
    sun: L.divIcon({
        className: 'custom-sun-icon',
        html: '<div style="font-size: 24px; color: gold; text-shadow: 0 0 3px rgba(0,0,0,0.5);">☀️</div>',
        iconSize: [30, 30],
        iconAnchor: [15, 15],
        popupAnchor: [0, -15]
    }),

    // Define the Custom DivIcon
    gps: L.divIcon({
        className: 'gps-marker', // Remove default wrapper styling
        html: '<div class="gps-pulse"></div><div class="gps-dot"></div>',
        iconSize: [35, 35],      // Container bounds
        iconAnchor: [17.5, 17.5] // Center the anchor exactly
    })
}
