import { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../AuthContext';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const response = await axios.post('http://localhost:8000/login', {
        username: username,
        password: password
      });
      login(response.data.token);
      navigate('/teams');
    } catch (err) {
      setError('Невірний логін або пароль ❌');
    }
  };

  return (
    <div className="container">
      <h2>Вхід у систему 🔒</h2>
      {error && <p style={{ color: '#cf6679' }}>{error}</p>}
      
      <form onSubmit={handleLogin}>
        <label>Логін:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
        
        <label>Пароль:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        
        <button type="submit">Увійти</button>
      </form>

      {}
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <Link to="/register" className="nav-link" style={{ fontSize: '14px', marginBottom: '0' }}>
          Немає акаунту? Зареєструйся!
        </Link>
      </div>
    </div>
  );
}