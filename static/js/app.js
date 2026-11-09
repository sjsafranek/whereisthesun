/**
 * App
 */
class App {
    constructor(container_id, options) {
        let self = this;
        this.options = options || {};

        this.api = new ApiClient("/");

        this.map = L.map(container_id, {
            center: [39.46, -94.65],
            zoom: 4,
        });

        this._layers = {
            'sunnyCities':  L.featureGroup(),
            'userMarker': L.marker([0, 0], { icon: Icons.gps }),
            'userAccuracy': L.circle([0, 0], {
                color: '#007bff',
                fillColor: '#007bff',
                fillOpacity: 0.15,
                weight: 1
            })
        };
        this._layers.userLocationFeatureGroup = L.featureGroup([this._layers.userMarker, this._layers.userAccuracy]);

        this._layers.sunnyCities.addTo(this.map);

        this.search_options = {
            min_population: 8000,
            max_cloud_cover: 30,
            limit: 1
        };

        L.control.searchOptionsControl({
            onSearchOptionsChange: function(search_options) {
                self.search_options = search_options;
                self.getUserLocation();
            }
        }).addTo(this.map);

        this.map.on('locationfound', (event) => self._onLocationFound(event) )
                .on('locationerror', console.log);
    
        this.getUserLocation(true);
    }

    _onLocationFound(event) {
        let self = this;
        this.setUserLocation(event.latlng, event.accuracy);
        this.findSunnyCities(event.latlng);
    }

    findSunnyCities(latlng) {
        let self = this;

        if (this.findSunnyCities.abort_controller) {
            this.findSunnyCities.abort_controller.abort();
        }
        this.findSunnyCities.abort_controller = new AbortController();
        
        this.options.onSearchStart && this.options.onSearchStart();
        let options = JSON.parse(JSON.stringify(this.search_options));
        options.signal = this.findSunnyCities.abort_controller.signal;
        
        this.api.findTheSun(latlng, options)
            .then((cities) => self.setSunnyCities(cities))
            .then(() => self.setMapBounds())
            .catch((error) => {
                if (error.name === 'AbortError') {
                    console.log('Fetch successfully canceled!');
                } else {
                    console.error('An actual network error occurred:', error);
                }
            })
            .finally(() => {
                self.options.onSearchEnd && this.options.onSearchEnd();
            });
    }

    getUserLocation(set_view) {
        // map.locate({setView: true, watch: true});
        this.map.locate({
            setView: set_view || false,
            maxZoom: 14
        });           
    }

    setUserLocation(latlng, accuracy) {
        this._layers.userMarker.setLatLng(latlng);
        this._layers.userAccuracy.setLatLng(latlng);
        this._layers.userAccuracy.setRadius(accuracy/2);
        !this.map.hasLayer(this._layers.userLocationFeatureGroup) && 
            this._layers.userLocationFeatureGroup.addTo(this.map);
    }

    _makeCityMarker(city) {
        return L.marker([city.latitude, city.longitude], { icon: Icons.sun }).bindPopup(city.name);
    }

    setSunnyCities(cities) {
        this._layers.sunnyCities.clearLayers();
        for (let i = 0; i < cities.length; i++) {
            let city = cities[i];
            const marker = this._makeCityMarker(city);
            this._layers.sunnyCities.addLayer(marker);
        }
    }

    setMapBounds() {
        const bounds = L.latLngBounds();
        bounds.extend(this._layers.sunnyCities.getBounds());
        bounds.extend(this._layers.userMarker.getLatLng());
        this.map.fitBounds(bounds, { maxZoom: 14 });
    }
}


/**
 * Search Options Control
 */
L.Control.SearchOptionsControl = L.Control.extend({
    options: {
        position: 'bottomright'
    },

    initialize: function(options) {
        L.Util.setOptions(this, options);
    },

    onAdd: function(map) {
        let self = this;

        // 1. Create a container DOM element
        var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
        container.style.backgroundColor = 'white';
        container.style.padding = '8px';
        container.style.cursor = 'pointer';

        // 2. Add HTML filter elements (e.g., a dropdown or button)
        container.innerHTML = `
            <div style="padding: 2px 4px">
                <label for="number-of-cities"><strong>Number of cities:</strong></label>
                <select id="number-of-cities" class="search-options-select">
                    <option value="1" selected>1</option>
                    <option value="5">5</option>
                    <option value="10">10</option>
                </select>
            </div>
            <div style="padding: 2px 4px">
                <label for="min-population"><strong>Min Population</strong></label>
                <select id="min-population" class="search-options-select">
                    <option value="0">0</option>
                    <option value="8000" selected>8,000</option>
                    <option value="16000">16,000</option>
                    <option value="32000">32,000</option>
                    <option value="64000">64,000</option>
                    <option value="128000">128,000</option>
                </select>
            </div>
            <div style="padding: 2px 4px">
                <label for="max-cloud-cover"><strong>Max clound cover</strong></label>
                <select id="max-cloud-cover" class="search-options-select">
                    <option value="10">10%</option>
                    <option value="20">20%</option>
                    <option value="30" selected>30%</option>
                    <option value="40">40%</option>
                    <option value="50">50%</option>
                </select>
            </div>                    
        `;

        // 3. Prevent map click events from firing when interacting with the control
        L.DomEvent.disableClickPropagation(container);

        // 4. Add event listener for filtering data
        container.querySelectorAll('.search-options-select').forEach(function(element) {
            L.DomEvent.on(element, 'change', function(e) {
                self.options.onSearchOptionsChange({
                    limit: parseInt(container.querySelector('#number-of-cities').value),
                    min_population: parseInt(container.querySelector('#min-population').value),
                    max_cloud_cover: parseInt(container.querySelector('#max-cloud-cover').value)
                }); 
            });
        });

        return container;
    },

    onRemove: function(map) {
        // Clean up event listeners if necessary to prevent memory leaks
    }
});

// Factory function
L.control.searchOptionsControl = function(opts) {
    return new L.Control.SearchOptionsControl(opts);
};
