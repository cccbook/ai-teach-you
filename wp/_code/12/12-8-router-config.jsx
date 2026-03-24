import { Routes, Route, Navigate } from 'react-router-dom';

const PrivateRoute = ({ children, isAuthenticated }) => (
  <Routes>
    <Route
      path="/"
      element={isAuthenticated ? children : <Navigate to="/login" />}
    />
  </Routes>
);

const Dashboard = () => <h1>Dashboard</h1>;
const Login = () => <h1>Login</h1>;

export { PrivateRoute, Dashboard, Login };
