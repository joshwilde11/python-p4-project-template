import React from 'react';

const RecipeCard = ({ recipe, image, simpleView }) => {
  console.log('Recipe:', recipe);
  console.log('Image:', image);

  const unwantedWords = ["Ingredients:", "Steps:"];

  // Remove unwanted words from ingredients
  let cleanedIngredients = recipe.ingredients || '';
  unwantedWords.forEach(word => {
    const regex = new RegExp(word, 'gi');
    cleanedIngredients = cleanedIngredients.replace(regex, '').trim();
  });

  const formattedIngredients = cleanedIngredients.replace(/\) /g, ')\n');

  // Remove unwanted words from steps
  let cleanedSteps = recipe.steps || '';
  unwantedWords.forEach(word => {
    const regex = new RegExp(word, 'gi');
    cleanedSteps = cleanedSteps.replace(regex, '').trim();
  });

  // Split steps by newline character to ensure each step has its own line
  const formattedSteps = cleanedSteps.split('\n').map((step, index) => (
    <p key={index}>{step}</p>
  ));

  // Extract the text after the colon in the title
  const titleAfterColon = recipe.title.split(':').pop().trim();

  return (
    <div className="recipe-card">
      {image && <img src={image} alt={`${titleAfterColon} image`} className="recipe-image" />}
      <h3>{titleAfterColon}</h3>
      {!simpleView && (
        <div>
          <p>{recipe.description}</p>
          <p>Ingredients:</p>
          <pre className="recipe-ingredients">{Array.isArray(recipe.ingredients) ? recipe.ingredients.join(', ') : formattedIngredients}</pre>
          <p>Instructions:</p>
          <div className="recipe-steps">{Array.isArray(recipe.instructions) ? recipe.instructions.join(', ') : formattedSteps}</div>
        </div>
      )}
    </div>
  );
};

export default RecipeCard;