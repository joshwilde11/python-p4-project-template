import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [retypePassword, setRetypePassword] = useState('');
  const history = useHistory();

  const handleLogin = async (e) => {
    e.preventDefault();

    const requestBody = { username, password };
    if (!username || !password) {
      alert("Username and password are required!");
      return;
    }

    if (retypePassword) {
      // Registration request
      if (password !== retypePassword) {
        alert("Passwords do not match!");
        return;
      }
      requestBody.retypePassword = retypePassword;
    }

    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('token', data.token); // Store token in local storage
      history.push('/grocery-store-list'); // Redirect to GroceryStoreList page
    } else {
      const errorData = await response.json();
      console.error('Error:', errorData.message);
      alert(errorData.message);
    }
  };

  return (
    <div className="container login-container">
      <h1>Welcome to Recipe Ripper.</h1>
      <p>We find weekly deals at your local grocer and make recipes to save you money. Sign in to get to cookin'!</p>
      <h2>Login</h2>
      <form onSubmit={handleLogin} className="login-form">
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Retype Password (new users only)</label>
          <input
            type="password"
            value={retypePassword}
            onChange={(e) => setRetypePassword(e.target.value)}
          />
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default Login;