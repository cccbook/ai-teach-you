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
