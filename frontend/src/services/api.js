import axios from 'axios';

const API_URL = 'http://localhost:8080';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Intercepteur pour ajouter le token JWT à chaque requête
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export const authAPI = {
    login: (email, password) => api.post('/auth/login', { email, password }),
    register: (userData) => api.post('/users/', userData),
    getMe: () => api.get('/auth/me'),
    changePassword: (data) => api.put('/auth/change-password', data),
};

export const accountAPI = {
    getUserAccounts: (userId) => api.get(`/accounts/user/${userId}`),
    createAccount: (data) => api.post('/accounts/', data),
    deposit: (accountId, amount) => api.post(`/accounts/${accountId}/deposit?amount=${amount}`),
    withdraw: (accountId, amount) => api.post(`/accounts/${accountId}/withdraw?amount=${amount}`),
    transfer: (fromId, toId, amount) => api.post(`/accounts/${fromId}/transfer?to_account_id=${toId}&amount=${amount}`),
};

export const transactionAPI = {
    getAccountTransactions: (accountId) => api.get(`/transactions/account/${accountId}`),
};

export default api;
