import { useState, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../AuthContext';

export default function AddTeamPage() {
  const [name, setName] = useState('');
  const [powerRating, setPowerRating] = useState('');
  const [error, setError] = useState('');
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();

  if (!token) {
    navigate('/login');
    return null;
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/teams/', {
        league_id: 1, 
        name: name,
        power_rating: parseFloat(powerRating)
      });
      navigate('/teams'); 
    } catch (err) {
      setError('Помилка при збереженні. Перевір бекенд.');
    }
  };

  return (
    <div className="container">
      <Link to="/teams" className="nav-link">← Назад до списку</Link>
      <h2>Нова команда 📝</h2>
      
      {error && <p style={{ color: '#cf6679' }}>{error}</p>}
      
      <form onSubmit={handleSubmit}>
        <label>Назва команди:</label>
        <input 
          type="text" 
          value={name} 
          onChange={(e) => setName(e.target.value)} 
          required 
        />
        
        <label>Power Rating (Рейтинг):</label>
        <input 
          type="number" 
          step="0.1" 
          value={powerRating} 
          onChange={(e) => setPowerRating(e.target.value)} 
          required 
        />
        
        <button type="submit">Зберегти команду</button>
      </form>
    </div>
  );
}