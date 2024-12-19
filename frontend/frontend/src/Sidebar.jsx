import React from "react";
import "./Sidebar.css";
import { Link } from 'react-router-dom';

const SidebarMenu = () => {
  return (
    <nav>
      <ul>
        <li><Link to="/logout">Выйти</Link></li>
        <li><Link to="/">Личная информация</Link></li>
        <li><Link to="/history">Медицинская история</Link></li>
        <li><Link to="/appointments">Записи</Link></li>
        </ul>
    </nav>
  );
};

export default SidebarMenu;
