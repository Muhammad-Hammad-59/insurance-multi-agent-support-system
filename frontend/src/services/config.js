// frontend/src/services/config.js
const config = {
    // Use environment variable or default to localhost for development
    API_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
    
    // Session timeout in milliseconds (1 hour)
    SESSION_TIMEOUT: 3600000,
    
    // Maximum retries for failed requests
    MAX_RETRIES: 3,
    
    // Retry delay in milliseconds
    RETRY_DELAY: 1000
};

export default config;