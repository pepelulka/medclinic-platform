import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";

const UnAuth = () => {
    const [loggedOut, setLoggedOut] = useState(false); 
    
    const navigate = useNavigate();

    fetch("http://localhost/api/logout", 
    {
        withCredentials: true
    }).then(() => {
        navigate("/")
        location.reload()
    });

    
    return (
        <p>Logging out...</p>
    );
};

export default UnAuth;