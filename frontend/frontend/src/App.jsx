import React, { useEffect, useState } from 'react';
import Cookies from 'js-cookie';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';

import ProfilePage from "./components/ProfilePage.jsx"
import PatientHistory from "./components/PatientHistory.jsx"

import SidebarMenu from "./Sidebar.jsx"
import AdminSidebarMenu from './AdminSidebar.jsx';
import AuthForm from './components/AuthForm.jsx';
import UnAuth from "./components/UnAuth.jsx";
import PatientRecords from './components/PatientRecords.jsx';
import { AddDoctor, AddPatient } from './components/AdminPanel.jsx';
import AppointmentsLogs from './components/AppointmentsLogs.jsx';
import { getBackendHost } from "./Settings.jsx"

function App() {

  const [authorized, setAuthorized] = useState(false)
  const [isAdmin, setIsAdmin] = useState(false)
  const [patientId, setPatientId] = useState(null)

  const BACKEND_HOST = getBackendHost();

  useEffect(() => {
    console.log(BACKEND_HOST)
    const localPatientId = Cookies.get('patient_id')

    if (localPatientId && localPatientId == 'admin') {
      setAuthorized(true);
      setIsAdmin(true);
    } else if (localPatientId && localPatientId != 'deleted') {
      setAuthorized(true);
      setPatientId(localPatientId);
    } else {
      setAuthorized(false);
      setPatientId(null);
      setIsAdmin(false);
    }
  })

  return (
    <>
    { authorized ? (
      <>
      {
        isAdmin ? (
          <Router>
            <div className="app" style={{ display: "flex", height: "100vh" }}>
              <AdminSidebarMenu />
              <Routes>
                <Route path="/logout" element={<UnAuth />} />
                <Route path="/patients/add" element={<AddPatient />} />
                <Route path="/doctors/add" element={<AddDoctor />} />
                <Route path="/logs" element={<AppointmentsLogs />} />
                </Routes>
            </div>
          </Router>
        ) : (
          <Router>
            <div className="app" style={{ display: "flex", height: "100vh" }}>
                <SidebarMenu /> {/* Боковая панель */}
                <Routes>
                    <Route path="/logout" element={<UnAuth />} />
                    <Route path="/" element={<ProfilePage />} />
                    <Route path="/history" element={<PatientHistory />} />
                    <Route path="/appointments" element={<PatientRecords />} />
                </Routes>
            </div>
        </Router>
        )
      }
      </>
    ) : ( <AuthForm /> )
    }
    </>
  );
}

export default App;