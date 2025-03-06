import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';

const DiscountedItems = () => {
  const [items, setItems] = useState([]);
  const history = useHistory();

  useEffect(() => {
    const fetchDiscountedItems = async () => {
      try {
        const response = await fetch('/api/discounted-items');
        const data = await response.json();
        setItems(data);
      } catch (error) {
        console.error('Error fetching discounted items:', error);
      }
    };

    fetchDiscountedItems();
  }, []);

  const handleShowRecipes = () => {
    history.push('/recipes');
  };

  const handleViewGroceryStores = () => {
    history.push('/grocery-store-list');
  };

  return (
    <div className="container">
      <div className="header">
        <img
          src="/images/left.png"
          alt="View Grocery Stores"
          onClick={handleViewGroceryStores}
          style={{ cursor: 'pointer', width: '24px', height: '24px' }}
        />
        <button
          onClick={handleShowRecipes}
          className="show-recipes-button">Generate Recipes</button>
      </div>
      <h2>Discounted Items</h2>
      <h3>Available between March 2nd and March 8th</h3>
      <ul>
        {items.map((item, index) => (
          <li key={index}>
            <strong>{item.name}</strong>: {item.discount}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default DiscountedItems;