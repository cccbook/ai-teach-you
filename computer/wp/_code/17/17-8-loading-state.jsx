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
