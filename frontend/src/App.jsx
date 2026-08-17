import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'
import { useEffect } from 'react';
// Recipe display function
// refreshKey is just a number passed in from App - changing it re-runs the fetch below
function RecipeList({ refreshKey }){
  // fetching the recipes from backend
  const[recipes, setRecipes] = useState([])

  // pulled out so both useEffect and the delete button can call it
  function fetchRecipes() {
    fetch('http://127.0.0.1:8000/recipes')
      .then(response => response.json())
      .then(data => setRecipes(data))
  }
  // On key refresh, fetches the recipes
  useEffect(() => {
    fetchRecipes()
  }, [refreshKey]);

  function handleDelete(id) {
    deleteRecipe(id).then(() => {
      fetchRecipes(); // refresh the list after a successful delete
    });
  }

  return(
    <div>
      {recipes.map(recipe => (
      <div key={recipe.id} className="ingredient-row">
        <span>
        {recipe.id}: {recipe.name}:
      <ul>
       {recipe.ingredients.map(ingredient => (
        <li key={ingredient.id}>{ingredient.id}: {ingredient.name}</li>
        ))}
        </ul>
        </span>
        <button onClick={() => handleDelete(recipe.id)}>Delete</button>
        </div>
      ))}
    </div>
  )
}
function addRecipe(name, owner, ingredientIds) {
  const params = new URLSearchParams();
  params.append('recipe_name', name);
  params.append('owner_name', owner);
  ingredientIds.forEach(id => params.append('ingredient_ids', id));

  return fetch(`http://127.0.0.1:8000/recipes?${params.toString()}`, {
    method: 'POST'
  })
    .then(response => response.json());
}
function deleteRecipe(id) {
  return fetch(`http://127.0.0.1:8000/recipes?id=${id}`, {
    method: 'DELETE'
  })
    .then(response => response.json());
}

// Form + button for adding a new recipe
// onAdded is a callback from App, called once the recipe is actually saved
function AddRecipeForm({ onAdded }) {
  const [name, setName] = useState('');
  const [owner, setOwner] = useState('');
  const [ingredientIdsText, setIngredientIdsText] = useState('');

  function handleSubmit() {
    // "1, 3, 4" -> [1, 3, 4]
    const ingredientIds = ingredientIdsText
      .split(',')
      .map(id => id.trim())
      .filter(id => id !== '')
      .map(Number);

    addRecipe(name, owner, ingredientIds).then(() => {
      onAdded();
    });
    setName('');
    setOwner('');
    setIngredientIdsText('');
  }

  return (
    <div>
      <input
        type="text"
        placeholder="Recipe name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <input
        type="text"
        placeholder="Owner"
        value={owner}
        onChange={e => setOwner(e.target.value)}
      />
      <input
        type="text"
        placeholder="Ingredient ids, comma separated (e.g. 1,3,4)"
        value={ingredientIdsText}
        onChange={e => setIngredientIdsText(e.target.value)}
      />
      <button onClick={handleSubmit}>Add Recipe</button>
    </div>
  );
}
// refreshKey is just a number passed in from App - changing it re-runs the fetch below
function IngredientList({ refreshKey }){
  const[ingredients, setIngredients] = useState([])

  // pulled out so both useEffect and the delete button can call it
  function fetchIngredients() {
    fetch('http://127.0.0.1:8000/ingredients')
      .then(response => response.json())
      .then(data => setIngredients(data))
  }

  useEffect(() => {
    fetchIngredients()
  }, [refreshKey]);

  function handleDelete(id) {
    deleteIngredient(id).then(() => {
      fetchIngredients(); // refresh the list after a successful delete
    });
  }

  return(
    <div>
      {ingredients.map(ingredient => (
        <p key={ingredient.id} className="ingredient-row">
          <span>{ingredient.name}:  ${ingredient.price}</span>
          <button onClick={() => handleDelete(ingredient.id)}>Delete</button>
        </p>
      ))}
    </div>
  )
}
function addIngredient(name, price) {
  const params = new URLSearchParams();
  params.append('foodname', name);
  params.append('foodprice', price);

  // return the fetch so callers can know when it's actually done
  return fetch(`http://127.0.0.1:8000/ingredients?${params.toString()}`, {
    method: 'POST'
  })
    .then(response => response.json());
}

function deleteIngredient(id) {
  const params = new URLSearchParams();
  params.append('id', id);

  return fetch(`http://127.0.0.1:8000/ingredients?${params.toString()}`, {
    method: 'DELETE'
  })
    .then(response => response.json());
}

// Form + button for adding a new ingredient
// onAdded is a callback from App, called once the ingredient is actually saved
function AddIngredientForm({ onAdded }) {
  const [name, setName] = useState('');
  const [price, setPrice] = useState('');

  function handleSubmit() {
    addIngredient(name, price).then(() => {
      onAdded();
    });
    setName('');
    setPrice('');
  }

  return (
    <div>
      <input
        type="text"
        placeholder="Ingredient name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <input
        type="number"
        placeholder="Price"
        value={price}
        onChange={e => setPrice(e.target.value)}
      />
      <button onClick={handleSubmit}>Add Ingredient</button>
    </div>
  );
}

function GroceryList(recipeIds, budget){
    const params = new URLSearchParams()
    params.append('budget', budget)
    recipeIds.forEach(id => params.append('recipe_ids', id));

    return fetch(`http://127.0.0.1:8000/list?${params.toString()}`, {
      method: 'POST'
    })
    
    .then(response => response.json())
    

  
}
function GroceryListForm({onAdded}){
  const [budget, setBudget] = useState(0)
  const [recipeIdsText, setRecipeIdsText] = useState('')
  // holds the generated grocery list once the backend responds - null means "nothing generated yet"
  const [result, setResult] = useState(null)

    function handleSubmit() {
    // "1, 3, 4" -> [1, 3, 4]
    const recipeIds = recipeIdsText
      .split(',')
      .map(id => id.trim())
      .filter(id => id !== '')
      .map(Number);

    // data here is the actual grocery list object the backend sent back -
    // we store it in state so it can be rendered, instead of throwing it away
    GroceryList(recipeIds, budget).then(data => {
      setResult(data);
      onAdded();
    });
    setBudget(0);
    setRecipeIdsText('');
  }
  return(
    <div>
    <input 
    type="number"
    placeholder="Budget"
    value={budget}
    onChange={e => setBudget(e.target.value)}
    />


    <input
    type="text"
    placeholder="Recipe ids, comma separated (e.g. 1,3,4)"
    value={recipeIdsText}
    onChange={e => setRecipeIdsText(e.target.value)}
    />
    <button onClick={handleSubmit}>Generate Grocery List</button>
    {result && (
    <div>
      <p>{result['Budget Message']}</p>
      <p>Total: {result['Total Price']}</p>
     <ul>
      {Object.entries(result)
      .filter(([key]) => key !== 'Total Price' && key !== 'Budget Message')
      .map(([name, price]) => (
      <li key={name}>{name}: ${price}</li>
    ))}
    </ul>



    </div>
    )}


    </div>

  )

}

function App() {
  // bumping this number tells RecipeList to refetch
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div>
      <h1>Recipe list</h1>
      <AddRecipeForm onAdded={() => setRefreshKey(prev => prev + 1)}></AddRecipeForm>
      <RecipeList refreshKey={refreshKey}></RecipeList>
      <h1>Grocery List</h1>
      <GroceryListForm onAdded={() => {}}></GroceryListForm>
    </div>
  );
}

export default App;
