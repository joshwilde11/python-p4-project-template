import React, { useState } from 'react';

const Pantry = () => {
  const [items, setItems] = useState(['']);

  const handleInputChange = (index, event) => {
    const newItems = [...items];
    newItems[index] = event.target.value;
    setItems(newItems);
  };

  const handleAddItem = () => {
    setItems([...items, '']);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleAddItem();
    }
  };

  return (
    <div className="pantry">
      <h1>Pantry</h1>
      <h3>Add some ingredients that you keep on hand so we can tailor our recipes to your taste!</h3>
      
      {items.map((item, index) => (
        <div key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
          <input
            type="text"
            value={item}
            onChange={(event) => handleInputChange(index, event)}
            onKeyPress={handleKeyPress}
            placeholder={`Item ${index + 1}`}
            style={{ marginRight: '10px' }}
          />
          {index === items.length - 1 && (
            <button onClick={handleAddItem}>Add</button>
          )}
        </div>
      ))}
    </div>
  );
};

export default Pantry;

