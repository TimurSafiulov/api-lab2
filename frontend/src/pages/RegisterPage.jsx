import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

export default function RegisterPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      await axios.post('http://localhost:8000/register', {
        username: username,
        password: password
      });
      
      setSuccess('Успіх! 🎉 Тепер можеш увійти.');
  
      setTimeout(() => navigate('/login'), 2000);
      
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setError('Користувач з таким логіном вже існує 😅');
      } else {
        setError('Помилка сервера. Перевір бекенд.');
      }
    }
  };

  return (
    <div className="container">
      <h2>Реєстрація 📝</h2>
      {error && <p style={{ color: '#cf6679' }}>{error}</p>}
      {success && <p style={{ color: '#03dac6', fontWeight: 'bold' }}>{success}</p>}
      
      <form onSubmit={handleRegister}>
        <label>Придумай логін:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} required />
        
        <label>Придумай пароль:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        
        <button type="submit">Зареєструватись</button>
      </form>
      
      <div style={{ marginTop: '20px', textAlign: 'center' }}>
        <Link to="/login" className="nav-link" style={{ fontSize: '14px', marginBottom: '0' }}>
          Вже є акаунт? Увійти
        </Link>
      </div>
    </div>
  );
}