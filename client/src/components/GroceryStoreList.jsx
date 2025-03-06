import React from 'react';
import { useHistory } from 'react-router-dom';
import GroceryStoreCard from './GroceryStoreCard';

const GroceryStoreList = () => {
  const history = useHistory();

  const handleWholeFoodsClick = () => {
    history.push('/discounted-items');
  };

  const handleBackToDiscounts = () => {
    history.push('/discounts');
  };

  const handleViewDiscounts = () => {
    history.push('/discounted-items');
  };

  const stores = [
    { name: 'Whole Foods', logo: '/images/wholefooods.png', clickable: true, onClick: handleWholeFoodsClick },
    { name: 'Trader Joe\'s', logo: '/images/trader.png', clickable: false },
    { name: 'Safeway', logo: '/images/safewayfr.png', clickable: false },
    { name: 'Kroger', logo: '/images/krogey.png', clickable: false },
    { name: 'Publix', logo: '/images/pubba.png', clickable: false },
    { name: 'Walmart', logo: '/images/walmart.png', clickable: false }
  ];

  return (
    <div className="container">
      <h1>Welcome to Recipe Ripper.</h1>
      <p>Pick a grocer to see what deals are available this week.</p>
      <h2>Grocery Store List</h2>
      <div className="store-list">
        {stores.map((store, index) => (
          <GroceryStoreCard
            key={index}
            name={store.name}
            logo={store.logo}
            clickable={store.clickable}
            onClick={store.onClick}
          />
        ))}
      </div>
    </div>
  );
};

export default GroceryStoreList;