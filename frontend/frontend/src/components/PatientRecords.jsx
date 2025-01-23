import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import "./ProfilePage.css"
import "./PatientRecords.css"
import { getBackendHost } from '../Settings.jsx'

const PatientRecords = () => {
  const patientId = Cookies.get('patient_id');
  const BACKEND_HOST = getBackendHost();

  const [appointments, setAppointments] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [clinics, setClinics] = useState([]);
  const [formData, setFormData] = useState({ patient_id: patientId, doctor_id: '', clinic_id: '', time: '' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
  
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Месяцы начинаются с 0
    const year = date.getFullYear();
  
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
  
    return `${day}.${month}.${year} ${hours}:${minutes}:${seconds}`;
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [appointmentsRes, doctorsRes, clinicsRes] = await Promise.all([
          axios.get(`${BACKEND_HOST}/api/appointments/${patientId}`),
          axios.get(`${BACKEND_HOST}/api/doctors`),
          axios.get(`${BACKEND_HOST}/api/clinics`),
        ]);

        setAppointments(appointmentsRes.data);
        setDoctors(doctorsRes.data);
        setClinics(clinicsRes.data);
      } catch (err) {
        setError('Failed to fetch data');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [patientId]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${BACKEND_HOST}/api/appointments/create`, formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      alert('Вы добавили новую запись!');
      setFormData({ patient_id: patientId, doctor_id: '', clinic_id: '', time: '' });
      // Optionally reload appointments
      const updatedAppointments = await axios.get(
        `${BACKEND_HOST}/api/appointments/${patientId}`
      );
      setAppointments(updatedAppointments.data);
    } catch (err) {
      alert('Не получилось добавить запись...');
    }
  };

  const deleteAppointment = async (appointmentId) => {
    await axios.delete(`${BACKEND_HOST}/api/appointments/delete/${appointmentId}`)
    const updatedAppointments = await axios.get(
      `${BACKEND_HOST}/api/appointments/${patientId}`
    );
    setAppointments(updatedAppointments.data);
  }

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

  return (
    <div style={{ flex: 1, padding: "1rem", overflowY: "auto"  }}>
      <h1>Мои записи</h1>
      <div className="appointments-container">
        <div className="appointments-content">
          <h2 className="appointments-subtitle">Записи</h2>
          {appointments.length > 0 ? (
            <ul className="appointments-list">
              {appointments.map((appointment) => (
                <li className="appointment-item" key={appointment.id}>
                  <strong>Врач:</strong> {appointment.doctor_name}, <strong>Адрес клиники:</strong> {appointment.clinic_address}, <strong>Время:</strong> {formatTimestamp(appointment.time)} <button onClick = { () => deleteAppointment(appointment.id) }>Удалить</button>
                </li>
              ))}
            </ul>
          ) : (
            <p className="no-appointments-message">У вас нет записей</p>
          )}
        </div>
      </div>
      <div>
        <h2>Добавить новую запись</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Врач:
            <select
              name="doctor_id"
              value={formData.doctor_id}
              onChange={handleInputChange}
              required
            >
              <option value="">Врач</option>
              {doctors.map((doctor) => (
                <option key={doctor.id} value={doctor.id}>
                  {doctor.name}
                </option>
              ))}
            </select>
          </label>
          <br />
          <label>
            Клиника:
            <select
              name="clinic_id"
              value={formData.clinic_id}
              onChange={handleInputChange}
              required
            >
              <option value="">Клиника</option>
              {clinics.map((clinic) => (
                <option key={clinic.id} value={clinic.id}>
                  {clinic.address}
                </option>
              ))}
            </select>
          </label>
          <br />
          <label>
            Время:
            <input
              type="datetime-local"
              name="time"
              value={formData.time}
              onChange={handleInputChange}
              required
            />
          </label>
          <br />
          <button type="submit">Добавить запись</button>
        </form>
      </div>
    </div>
  );
};

export default PatientRecords;