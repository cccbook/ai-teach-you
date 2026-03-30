# 第 17 章：前後端整合

## 概述

本章介紹如何將 React 前端與 FastAPI 後端整合，解決 CORS、API 串接、環境配置等問題。

## 17.1 CORS 設定

配置跨來源資源共享以允許前後端通訊。

[程式檔案：17-1-cors-setup.py](../_code/17/17-1-cors-setup.py)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/hello")
async def hello():
    return {"message": "Hello from FastAPI"}

@app.get("/api/data")
async def get_data():
    return {"items": [{"id": 1, "name": "Item 1"}]}

@app.post("/api/data")
async def create_data(data: dict):
    return {"created": data, "status": "success"}
```

## 17.2 React 發送請求

使用 fetch API 從 React 發送 HTTP 請求。

[程式檔案：17-2-fetch-from-react.jsx](../_code/17/17-2-fetch-from-react.jsx)

```javascript
import { useState, useEffect } from 'react';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const useApi = (endpoint, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });
      
      if (!response.ok) throw new Error('Network response was not ok');
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (options.method !== 'POST' && options.method !== 'PUT') {
      fetchData();
    }
  }, [endpoint]);

  return { data, loading, error, fetchData };
};

export default useApi;
```

## 17.3 Axios 配置

使用 Axios 簡化 HTTP 請求處理。

[程式檔案：17-3-axios-setup.jsx](../_code/17/17-3-axios-setup.jsx)

```javascript
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const get = (url, config) => api.get(url, config);
export const post = (url, data, config) => api.post(url, data, config);
export const put = (url, data, config) => api.put(url, data, config);
export const del = (url, config) => api.delete(url, config);

export default api;
```

## 17.4 API 服務封裝

建立統一的 API 服務模組。

[程式檔案：17-4-api-service.js](../_code/17/17-4-api-service.js)

```javascript
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
```

## 17.5 環境變數配置

使用環境變數管理不同環境的配置。

[程式檔案：17-5-env-config.js](../_code/17/17-5-env-config.js)

```javascript
# Frontend (.env)
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development

# Vite (.env)
VITE_API_URL=http://localhost:8000

# Usage in code
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const fetchItems = async () => {
  const response = await fetch(`${API_URL}/items`);
  return response.json();
};
```

## 17.6 代理設定

使用 Vite 或 Webpack 代理設定避免 CORS 問題。

[程式檔案：17-6-proxy-config.js](../_code/17/17-6-proxy-config.js)

```javascript
# Vite proxy (vite.config.js)
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});

# Usage - no CORS issues!
const response = await fetch('/api/items');
```

## 17.7 React 錯誤處理

建立統一的錯誤處理機制。

[程式檔案：17-7-error-handling-react.jsx](../_code/17/17-7-error-handling-react.jsx)

```javascript
import { useState } from 'react';
import api from './17-3-axios-setup.jsx';

export const useApiRequest = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = async (apiCall, ...args) => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiCall(...args);
      return response.data;
    } catch (err) {
      const message = err.response?.data?.detail || err.message;
      setError(message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { request, loading, error };
};

export const ErrorMessage = ({ error }) => {
  if (!error) return null;
  
  if (typeof error === 'string') {
    return <div className="error">{error}</div>;
  }
  
  return (
    <div className="error">
      {error.message || 'An error occurred'}
    </div>
  );
};

export default useApiRequest;
```

## 17.8 載入狀態處理

提供良好的載入體驗。

[程式檔案：17-8-loading-state.jsx](../_code/17/17-8-loading-state.jsx)

```javascript
import { useState, useEffect } from 'react';

export const LoadingSpinner = () => (
  <div className="spinner">Loading...</div>
);

export const LoadingOverlay = ({ isLoading, children }) => {
  if (!isLoading) return children;
  
  return (
    <div className="loading-overlay">
      <div className="spinner" />
    </div>
  );
};

export const useLoadingState = (asyncFn, deps = []) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let mounted = true;
    
    const fetch = async () => {
      setLoading(true);
      try {
        const result = await asyncFn();
        if (mounted) setData(result);
      } catch (err) {
        if (mounted) setError(err);
      } finally {
        if (mounted) setLoading(false);
      }
    };
    
    fetch();
    return () => { mounted = false; };
  }, deps);

  return { loading, data, error };
};

export default LoadingSpinner;
```

## 17.9 認證攔截器

自動處理 JWT Token 刷新。

[程式檔案：17-9-auth-interceptor.js](../_code/17/17-9-auth-interceptor.js)

```javascript
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
```

## 17.10 完整專案結構

[程式檔案：17-10-fullstack-structure.md](../_code/17/17-10-fullstack-structure.md)

```markdown
# Full-Stack Project Structure

my-fullstack-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   └── services/
│   ├── tests/
│   ├── alembic/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── context/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── package.json
│   └── .env
│
├── docker-compose.yml
└── README.md
```

## 重點回顧

| 概念 | 說明 |
|------|------|
| CORS | 跨來源資源共享配置 |
| fetch | 原生 HTTP 請求 API |
| Axios | HTTP 客戶端庫 |
| 環境變數 | 不同環境配置管理 |
| 代理 | 開發環境避免 CORS |
| 攔截器 | 統一處理請求/回應 |

## 練習題

1. 建立完整的 API 服務層
2. 實作統一的錯誤處理系統
3. 建立登入/登出流程
4. 實作 Token 自動刷新機制
