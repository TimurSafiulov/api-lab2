import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import LoginPage from './pages/LoginPage';
import TeamsPage from './pages/TeamsPage';
import AddTeamPage from './pages/AddTeamPage';
import RegisterPage from './pages/RegisterPage'; 
import './index.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} /> {}
          <Route path="/teams" element={<TeamsPage />} />
          <Route path="/add-team" element={<AddTeamPage />} />
          <Route path="*" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;