import React from 'react';

const GroceryStoreCard = ({ name, logo, clickable, onClick }) => {
  return (
    <div className={`grocery-store-card ${clickable ? 'clickable' : ''}`} onClick={clickable ? onClick : null}>
      <img src={logo} alt={`${name} logo`} className="grocery-store-logo" />
      <p>{name}</p>
    </div>
  );
};

export default GroceryStoreCard;