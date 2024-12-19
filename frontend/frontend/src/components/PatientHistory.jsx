import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import './PatientHistory.css';

const PatientHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const patientId = Cookies.get('patient_id');

    const fetchHistory = async () => {
      try {
        const response = await fetch(`http://localhost/api/history/${patientId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch patient history.');
        }
        const data = await response.json();
        setHistory(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, [navigate]);

  if (loading) return <div className="loader">Loading...</div>;
  if (error) return <div className="error">Error: {error}</div>;

  const typeToRussianName = {
    "diagnosis": "Заключение",
    "test": "Анализ",
    "recovery": "Выздоровление"
  };

  return (
    <div className="patient-history">
      <h1>Медицинская история</h1>
      {history.length === 0 ? (
        <p>Нет записей...</p>
      ) : (
        <ul className="history-list">
          {history.map((record, index) => (
            <li key={index} className="history-item">
              <div className="doctor-name">Ответственный врач: {record.doctor_name}</div>
              <div className={`event-type event-${record.type}`}>{ typeToRussianName[record.type] }</div>
              <div className="description">Подробнее: {record.description}</div>
              <div className="record-time">Время: {new Date(record.record_time).toLocaleString()}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default PatientHistory;
