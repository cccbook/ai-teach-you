import api from './17-3-axios-setup.jsx';

export const ApiService = {
  items: {
    list: (params) => api.get('/items', { params }),
    get: (id) => api.get(`/items/${id}`),
    create: (data) => api.post('/items', data),
    update: (id, data) => api.put(`/items/${id}`, data),
    delete: (id) => api.delete(`/items/${id}`),
  },
  
  auth: {
    login: (credentials) => api.post('/token', credentials),
    register: (data) => api.post('/register', data),
    me: () => api.get('/users/me'),
    refresh: (token) => api.post('/refresh', { refresh: token }),
  },
  
  users: {
    list: () => api.get('/users'),
    get: (id) => api.get(`/users/${id}`),
    create: (data) => api.post('/users', data),
    update: (id, data) => api.put(`/users/${id}`, data),
    delete: (id) => api.delete(`/users/${id}`),
  },
};

export default ApiService;
