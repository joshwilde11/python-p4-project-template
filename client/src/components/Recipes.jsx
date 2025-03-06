import React, { useEffect, useState } from 'react';
import { useHistory } from 'react-router-dom';
import RecipeCard from './recipe_card';

const Recipes = () => {
  const [recipes, setRecipes] = useState([]);
  const history = useHistory();

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const response = await fetch('/api/recipes');
        const data = await response.json();
        if (Array.isArray(data)) {
          setRecipes(data);
        } else {
          console.error('API response is not an array:', data);
        }
      } catch (error) {
        console.error('Error fetching recipes:', error);
      }
    };

    fetchRecipes();
  }, []);

  const images = [
    '/images/choppa.jpg',
    '/images/fish.jpg',
    '/images/pasta.jpg'
  ];

  const handleCardClick = (recipe, image) => {
    history.push({
      pathname: `/recipes/${recipe.id}`,
      state: { recipe, image }
    });
  };

  const handleViewDiscounts = () => {
    history.push('/discounted-items');
  };

  return (
    <div className="container">
      <div className="header">
        <img
          src="/images/left.png"
          alt="View Discounts"
          onClick={handleViewDiscounts}
          style={{ cursor: 'pointer', width: '24px', height: '24px' }}
        />
      </div>
      <h2>Recipes</h2>
      <div className="recipe-card-container">
        {recipes.map((recipe, index) => (
          <div key={index} onClick={() => handleCardClick(recipe, images[index % images.length])}>
            <RecipeCard
              recipe={recipe}
              image={images[index % images.length]} // Cycle through images
              simpleView={true} // Pass the simpleView prop
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recipes;