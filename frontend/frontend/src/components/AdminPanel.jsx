import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminPanel.css'; // Добавим стили отдельно
import { getBackendHost } from '../Settings.jsx'

export const AddPatient = () => {
  const BACKEND_HOST = getBackendHost();

  const [patientInfo, setPatientInfo] = useState({
    name: '',
    phone_number: '',
    email: '',
    insurance_number: '',
  });

  const [userLogin, setUserLogin] = useState({
    login: '',
    password: '',
  });

  const handleAddPatient = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${BACKEND_HOST}/api/patients/add`, {
        patient_info: patientInfo,
        user_login: userLogin,
      });
      alert('Пациент успешно добавлен!');
      setPatientInfo({ name: '', phone_number: '', email: '', insurance_number: '' });
      setUserLogin({ login: '', password: '' });
    } catch (error) {
      console.error('Ошибка добавления пациента:', error);
      alert('Не удалось добавить пациента.');
    }
  };

  return (
    <div className="admin-panel">
    <section className="form-section">
      <h2 className='text-2xl font-bold pb-6'>Добавить пациента</h2>
      <form onSubmit={handleAddPatient} className="form flex justify-center w-full space-y-4">
        <input
          type="text"
          placeholder="Имя"
          value={patientInfo.name}
          onChange={(e) => setPatientInfo({ ...patientInfo, name: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Телефон"
          value={patientInfo.phone_number}
          onChange={(e) => setPatientInfo({ ...patientInfo, phone_number: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={patientInfo.email}
          onChange={(e) => setPatientInfo({ ...patientInfo, email: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Страховой номер"
          value={patientInfo.insurance_number}
          onChange={(e) => setPatientInfo({ ...patientInfo, insurance_number: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Логин"
          value={userLogin.login}
          onChange={(e) => setUserLogin({ ...userLogin, login: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Пароль"
          value={userLogin.password}
          onChange={(e) => setUserLogin({ ...userLogin, password: e.target.value })}
          required
        />
        <button type="submit">Добавить пациента</button>
      </form>
    </section>
    </div>
  );
};

export const AddDoctor = () => {
  const [doctorInfo, setDoctorInfo] = useState({
    name: '',
    speciality: '',
    experience: '',
    email: '',
    phone_number: '',
  });

  const [specialities, setSpecialities] = useState([]);

  useEffect(() => {
    // Получение списка специальностей врачей
    axios.get(`${BACKEND_HOST}/api/specialities`)
      .then(response => setSpecialities(response.data))
      .catch(error => console.error('Ошибка загрузки специальностей:', error));
  }, []);

  const handleAddDoctor = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${BACKEND_HOST}/api/doctors/add`, doctorInfo);
      alert('Врач успешно добавлен!');
      setDoctorInfo({ name: '', speciality: '', experience: '', email: '', phone_number: '' });
    } catch (error) {
      console.error('Ошибка добавления врача:', error);
      alert('Не удалось добавить врача.');
    }
  };

  return (
    <div className="admin-panel">
    <section className="form-section">
      <h2>Добавить врача</h2>
      <form onSubmit={handleAddDoctor} className="form">
        <input
          type="text"
          placeholder="Имя"
          value={doctorInfo.name}
          onChange={(e) => setDoctorInfo({ ...doctorInfo, name: e.target.value })}
          required
        />
        <select
          value={doctorInfo.speciality}
          onChange={(e) => setDoctorInfo({ ...doctorInfo, speciality: e.target.value })}
          required
        >
          <option value="">Выберите специальность</option>
          {specialities.map((speciality) => (
            <option key={speciality.name} value={speciality.name}>{speciality.name}</option>
          ))}
        </select>
        <input
          type="number"
          placeholder="Опыт (лет)"
          value={doctorInfo.experience}
          onChange={(e) => setDoctorInfo({ ...doctorInfo, experience: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={doctorInfo.email}
          onChange={(e) => setDoctorInfo({ ...doctorInfo, email: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Телефон"
          value={doctorInfo.phone_number}
          onChange={(e) => setDoctorInfo({ ...doctorInfo, phone_number: e.target.value })}
          required
        />
        <button type="submit">Добавить врача</button>
      </form>
    </section>
    </div>
  );
};
