import React, { useState } from 'react';
import './AuthForm.css';

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    login: '',
    password: '',
    confirmPassword: '',
  });
  const [authErrorMessage, setAuthErrorMessage] = useState("");

  const toggleMode = () => {
    setIsLogin((prev) => !prev);
    setFormData({ login: '', password: '', confirmPassword: '' });
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isLogin && formData.password !== formData.confirmPassword) {
      alert('Passwords do not match!');
      return;
    }

    if (isLogin) {
        fetch("http://localhost/api/login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Access-Control-Allow-Origin": "http://localhost",
              "Access-Control-Allow-Credentials": true
            },
            withCredentials: true,
            body: JSON.stringify({ login: formData.login, password: formData.password }),
        }).then(response => {
          if (response.status == 401) {
            setAuthErrorMessage("Неверные логин или пароль")
          } else {
            location.reload()
          }
        }).catch(err => {
          console.log(err)
        })
    }
    console.log(isLogin ? 'Logging in...' : 'Registering...', formData);
  };

  return (
    <div className="auth-container">
      <form className="auth-form" onSubmit={handleSubmit}>
        <h2>{isLogin ? 'Войти' : 'Register'}</h2>
        <p>{authErrorMessage}</p>
        <div className="form-group">
          <label htmlFor="login">Логин</label>
          <input
            type="text"
            id="login"
            name="login"
            value={formData.login}
            onChange={handleChange}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Пароль</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>
        {!isLogin && (
          <div className="form-group">
            <label htmlFor="confirmPassword">Confirm Password</label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
            />
          </div>
        )}
        <button type="submit" className="auth-button">
          {isLogin ? 'Войти' : 'Register'}
        </button>
      </form>
    </div>
  );
};

export default AuthForm;