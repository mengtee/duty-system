import axios from 'axios';

const apiClient = axios.create({
    baseURL: process.env.VUE_APP_API_URL || 'https://duty-system-production.up.railway.app',
    headers: {
        'Content-Type': 'application/json'
    }
});

export default apiClient;
