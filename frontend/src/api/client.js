import axios from 'axios';

console.log('VUE_APP_API_URL:', process.env.VUE_APP_API_URL);

const apiClient = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

export default apiClient;
