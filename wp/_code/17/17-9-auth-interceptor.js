import api from './17-3-axios-setup.jsx';

const TOKEN_KEY = 'access_token';
const REFRESH_KEY = 'refresh_token';

export const authInterceptor = (api) => {
  const interceptorId = api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem(TOKEN_KEY);
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );
  return interceptorId;
};

export const refreshInterceptor = (api) => {
  let isRefreshing = false;
  let failedQueue = [];

  const processQueue = (error, token = null) => {
    failedQueue.forEach(prom => {
      if (error) prom.reject(error);
      else prom.resolve(token);
    });
    failedQueue = [];
  };

  const interceptorId = api.interceptors.response.use(
    (response) => response,
    async (error) => {
      const originalRequest = error.config;
      
      if (error.response?.status === 401 && !originalRequest._retry) {
        if (isRefreshing) {
          return new Promise((resolve, reject) => {
            failedQueue.push({ resolve, reject });
          }).then(token => {
            originalRequest.headers.Authorization = `Bearer ${token}`;
            return api(originalRequest);
          });
        }
        
        originalRequest._retry = true;
        isRefreshing = true;
        
        try {
          const refreshToken = localStorage.getItem(REFRESH_KEY);
          const { data } = await api.post('/refresh', { refresh: refreshToken });
          localStorage.setItem(TOKEN_KEY, data.access_token);
          api.defaults.headers.common.Authorization = `Bearer ${data.access_token}`;
          processQueue(null, data.access_token);
          originalRequest.headers.Authorization = `Bearer ${data.access_token}`;
          return api(originalRequest);
        } catch (err) {
          processQueue(err, null);
          localStorage.removeItem(TOKEN_KEY);
          localStorage.removeItem(REFRESH_KEY);
          window.location.href = '/login';
          return Promise.reject(err);
        } finally {
          isRefreshing = false;
        }
      }
      return Promise.reject(error);
    }
  );
  return interceptorId;
};

export default authInterceptor;
