import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import { useEffect } from 'react';
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
      <IngredientList>

      </IngredientList>
    </div>
  );
}

export default App;
