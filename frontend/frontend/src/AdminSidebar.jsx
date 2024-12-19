import React from "react";
import "./Sidebar.css";
import { Link } from 'react-router-dom';

const AdminSidebarMenu = () => {
  return (
    <nav className='flex'>
      <ul>
        <li><Link to="/logout">Выйти</Link></li>
        <li><Link to="/patients/add">Добавить пациента</Link></li>
        <li><Link to="/doctors/add">Добавить врача</Link></li>
        <li><Link to="/logs">Журнал записей</Link></li>
      </ul>
    </nav>
  );
};

export default AdminSidebarMenu;
