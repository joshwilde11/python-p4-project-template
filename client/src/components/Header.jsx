import React from 'react';
import { useHistory, useLocation } from 'react-router-dom';

const Header = () => {
  const history = useHistory();
  const location = useLocation();

  const handleLogout = () => {
    // Add your logout logic here
    alert('Logged out!');
    history.push('/login');
  };

  // Do not show the log out button on the login page
  if (location.pathname === '/login') {
    return null;
  }

  return (
    <div className="container">
      <header>
        <img
          src="/images/logger.png"
          alt="Log Out"
          onClick={handleLogout}
          style={{ cursor: 'pointer', width: '24px', height: '24px' }}
        />
      </header>
    </div>
  );
};

export default Header;