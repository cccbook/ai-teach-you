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
