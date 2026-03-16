import { useState, useEffect, useContext } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../AuthContext';

export default function TeamsPage() {
  const [teams, setTeams] = useState([]);
  const [error, setError] = useState('');
  const { token, logout } = useContext(AuthContext);
  const navigate = useNavigate();

ъ
  useEffect(() => {
ё
    if (!token) {
      navigate('/login');
      return;
    }


    const fetchTeams = async () => {
      try {
        const response = await axios.get('http://localhost:8000/teams/');
        setTeams(response.data); 
      } catch (err) {
        setError('Не вдалося завантажити список команд. Перевір, чи працює бекенд!');
        console.error(err);
      }
    };

    fetchTeams();
  }, [token, navigate]);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Команди ⚽️</h2>
        <button onClick={handleLogout} className="btn-danger">Вийти</button>
      </div>
      
      <Link to="/add-team" className="nav-link">+ Додати нову команду</Link>
      
      {error && <p style={{ color: '#cf6679' }}>{error}</p>}
      
      <div>
        {teams.length === 0 && !error ? <p>Завантаження або команд немає...</p> : null}
        
        {teams.map((team) => (
          <div key={team.id} className="team-card">
            <span style={{ fontSize: '18px', fontWeight: 'bold' }}>{team.name}</span>
            <span style={{ color: '#03dac6', fontWeight: 'bold' }}>⭐ {team.power_rating}</span>
          </div>
        ))}
      </div>
    </div>
  );
}