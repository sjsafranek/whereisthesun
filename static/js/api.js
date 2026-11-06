
class ApiClient {
    /**
     * @param {string} baseUrl - The base URL for the API (e.g., 'https://example.com')
     * @param {Object} [config={}] - Optional configuration defaults
     */
    constructor(baseUrl, config = {}) {
        this.baseUrl = baseUrl.replace(/\/$/, '');
        this.defaultHeaders = config.headers || {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        };
        this.authToken = config.authToken || null;
    }

    generateUniqueId() {
        return Date.now().toString(36) + Math.random().toString(36).slice(2);
    }

    buildApiRequest(latlng, options) {
        options = options || {}
        return {
            method: 'FindTheSun',
            params: {
                latitude: latlng.lat,
                longitude: latlng.lng,
                min_population: options.min_population,
                max_cloud_cover: options.max_cloud_cover,
                limit: options.limit
            },
            id: this.generateUniqueId()
        };
    }

    findTheSun(latlng, options) {
        let payload = this.buildApiRequest(latlng, options);
        return fetch(`${this.baseUrl}/api/v1`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            })
            .then(response => response.json())
            .then(response => {
                if ('ok' == response.status)
                    return response.data.cities;
                throw new Error(response.error.message);
            });
    }
}
