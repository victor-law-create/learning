import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:8000/api', // This will be the base URL of our Django backend
});

export default API;
