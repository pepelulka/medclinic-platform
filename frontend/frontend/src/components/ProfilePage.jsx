import React, { useState, useEffect } from "react";
import "./ProfilePage.css"
import { getBackendHost } from '../Settings.jsx'

const ProfilePage = () => {
  const BACKEND_HOST = getBackendHost();

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  };

  const [userDataFetched, setUserDataFetched] = useState(false)
  const [userData, setUserData] = useState({
    "name": "",
    "phone_number": "",
    "email": "",
    "insurance_number": ""
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState(userData);

  useEffect(() => {
    const patientId = getCookie("patient_id");

    if (!patientId) {
      setError("Patient ID cookie not found.");
      setLoading(false);
      return;
    }

    // Отправляем GET-запрос с patient_id как user_id
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost/api/patients/${patientId}`);
        const data = await response.json();
        setUserDataFetched(true);
        setUserData(data);
        setFormData(data);
      } catch (err) {
        setError(`Error fetching user data. ${err}`);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSave = () => {
    const patientId = getCookie("patient_id");

    fetch(`http://localhost/api/patients/${patientId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Failed to update user data");
      })
      .then((updatedData) => {
        setUserData(formData);
        setIsEditing(false);
      })
      .catch((error) => console.error("Error updating user data:", error));
  };

  return (
    <div style={{ display: "flex", height: "100vh", margin: "0" }}>
      <main style={{ flex: 1, padding: "1rem", overflowY: "auto" }}>
        {error && (<p style={{ color: 'red' }}>{error}</p>) }
        {userDataFetched && (
        <>
        <h1>Личная информация</h1>
        {isEditing ? (
          <div className='leading-3 flex-col'>
            <label>
              Имя:
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Номер телефона:
              <input
                type="text"
                name="phone_number"
                value={formData.phone_number}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Электронная почта:
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Страховой номер:
              <input
                type="text"
                name="insurance_number"
                value={formData.insurance_number}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <button onClick={handleSave}>Сохранить</button>
            <button onClick={() => setIsEditing(false)}>Отмена</button>
          </div>
        ) : (
          <div className='leading-10'>
            <p><strong>Имя:</strong> {userData.name}</p>
            <p><strong>Номер телефона:</strong> {userData.phone_number}</p>
            <p><strong>Электронная почта:</strong> {userData.email}</p>
            <p><strong>Номер полиса:</strong> {userData.insurance_number}</p>
            <button onClick={() => setIsEditing(true)}>Редактировать</button>
          </div>

        )}
      </>
      )}
      </main>
    </div>
  );
};

export default ProfilePage;