import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import { useEffect } from 'react';
function RecipeList(){
  const[recipes, setRecipes] = useState([])
  useEffect(() => {
    fetch('http://127.0.0.1:8000/recipes')
      .then(response => response.json())
      .then(data => setRecipes(data))
  }, []);
  return(
    <div>
      {recipes.map(recipe => (
        <p key={recipe.id}>{recipe.name}: 
         <ul>
            {recipe.ingredients.map(ingredient => (
                <li key={ingredient.id}>{ingredient.name}</li>
            ))}
        </ul>
        </p>
      ))}
    </div>
  )
}
function IngredientList(){
  const[ingredients, setIngredients] = useState([])
  useEffect(() => {
    fetch('http://127.0.0.1:8000/ingredients')
      .then(response => response.json())
      .then(data => setIngredients(data))
  }, []);
  return(
    <div>
      {ingredients.map(ingredient => (
        <p key={ingredient.id}>{ingredient.name}:  ${ingredient.price}</p>
      ))}
    </div>
  )
}

function App() {
  return (
    <div>
      <h1>Ingredients list</h1>
      <RecipeList>

      </RecipeList>
    </div>
  );
}

export default App;
