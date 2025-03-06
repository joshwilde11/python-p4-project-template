import React from 'react';
import { useLocation, useHistory } from 'react-router-dom';
import RecipeCard from './recipe_card';

const RecipeDetail = () => {
  const location = useLocation();
  const history = useHistory();
  const { recipe, image } = location.state;

  const handleBackToRecipes = () => {
    history.push('/recipes');
  };

  return (
    <div className="container">
      <img
          src="/images/left.png"
          alt="View Discounts"
          onClick={handleBackToRecipes}
          style={{ cursor: 'pointer', width: '24px', height: '24px' }}
        />
      <RecipeCard recipe={recipe} image={image} />
    </div>
  );
};

export default RecipeDetail;