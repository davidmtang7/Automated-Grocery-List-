from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship
# Creates web app object
app = FastAPI()
# Allows the frontend (running on a different port) to fetch from this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
# Creates table for Recipe to Ingredient link, inherits sql model
class RecipeIngredient(SQLModel, table=True):
    recipe_id: int = Field(foreign_key="recipe.id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredient.id", primary_key=True)
# Ingredient Table, TO DO: ADD BRAND TO INGREDIENT AND FIX CURRENT INGREDIENTS TO MATCH
class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    # Recipe Table
class Recipe(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    owner: str
    ingredients: list["Ingredient"] = Relationship(link_model=RecipeIngredient)
# Creates engine to link to database
engine = create_engine("sqlite:///database.db")
# Creates the database
SQLModel.metadata.create_all(engine)

# Creates default tables in database
def seed():
    with Session(engine) as session:
        # Clears the database on startup
        # TO DO, UNCLEAR WHEN DROPPING APP 
        session.query(RecipeIngredient).delete()
        session.query(Recipe).delete()
        session.query(Ingredient).delete()
        session.commit()
        # 13 oz sausage
        sausage = Ingredient(name="Sausage", price= 4)
        # 12 ct eggs
        eggs = Ingredient(name="Eggs", price=2)
        # Barillas
        rigatoni = Ingredient(name="Rigatoni", price=1.89)
        # smallest possible
        mincedGarlic = Ingredient(name="Minced Garlic", price=2)
        heavyCream =  Ingredient(name="Heavy Cream", price=2.96)
        # bagged
        parmesanCheese = Ingredient(name="Parmesan Cheese", price=2)
        session.add_all([sausage, eggs, rigatoni, mincedGarlic, heavyCream, parmesanCheese])
        session.commit()


        # Liberty special pasta
        libertyrecipe = Recipe(name="Liberty Special Pasta", owner="Liberty")
        session.add(libertyrecipe)
        breakfast = Recipe(name="Breakfast Scramble", owner="David")
        session.add(breakfast)
        session.commit()

        # Add ingredient to recipes
        session.add_all([
        RecipeIngredient(recipe_id=libertyrecipe.id, ingredient_id = sausage.id),
        RecipeIngredient(recipe_id=libertyrecipe.id, ingredient_id = rigatoni.id),
        RecipeIngredient(recipe_id=libertyrecipe.id, ingredient_id = heavyCream.id),
        RecipeIngredient(recipe_id=libertyrecipe.id, ingredient_id = mincedGarlic.id),
        RecipeIngredient(recipe_id=libertyrecipe.id, ingredient_id = parmesanCheese.id),
        RecipeIngredient(recipe_id=breakfast.id, ingredient_id = sausage.id),
        RecipeIngredient(recipe_id=breakfast.id, ingredient_id = eggs.id),
        RecipeIngredient(recipe_id=breakfast.id, ingredient_id = parmesanCheese.id)
        ]
        )
        session.commit()
# Loads database on startup
@app.on_event("startup")
def on_startup():
    seed()
# Main menu
@app.get("/")
async def root():
    return ["This is grocery list app!!!"]

# Adding ingredients
@app.post("/ingredients")
def add_ingredients(foodname: str, foodprice: float):
    with Session(engine) as session:
        food = Ingredient(name=foodname, price=foodprice)
        session.add(food)
        session.commit()
    return 'Successful add!'

# Getting all ingredients
@app.get("/ingredients")
def get_ingredients():
    with Session(engine) as session:
        # returns whole ingredient database
        ingredients = session.exec(select(Ingredient)).all()
        return ingredients
# Deleting an ingredient 
@app.delete("/ingredients")
def del_ingredients(id : int):
    with Session(engine) as session:
        deleted = session.exec(select(Ingredient).where(Ingredient.id == id)).first()
        if deleted is None:
            return 'Ingredient not found'
        session.delete(deleted)
        session.commit()
    return 'Successful Delete!'


# Adding a recipe
@app.post("/recipes")
def add_recipes(ingredient_ids : list[int], recipe_name : str, owner_name : str):
    with Session(engine) as session:
        ingredients = session.exec(select(Ingredient).where(Ingredient.id.in_(ingredient_ids))).all()
        recipe = Recipe(name = recipe_name, owner=owner_name, ingredients=ingredients)
        session.add(recipe)
        session.commit()
        return 'Successful add!'
# Getting all recipes
@app.get("/recipes")
def get_recipes():
    with Session(engine) as session:
        #loads in recipes from database
        recipes = session.exec(select(Recipe)).all()
        #holds result for ingredients to fill
        result = []
        # for loop to append formatted data from each recipe to result
        for recipe in recipes:
        # formatting for current recipe
            result.append({
                "id": recipe.id,
                "name": recipe.name,
                "owner": recipe.owner,
                "ingredients": recipe.ingredients
            })
        return result
@app.delete("/recipes")
def del_recipes(id : int):
    with Session(engine) as session:
        # Deleting all the ingredient/recipe links
        links = session.exec(select(RecipeIngredient).where(RecipeIngredient.recipe_id == id)).all()
        for link in links:
            session.delete(link)
        # Deleting the Recipe
        deleted = session.exec(select(Recipe).where(Recipe.id == id)).first()
        if deleted is None:
            return 'Recipe not found'
        session.delete(deleted)
        session.commit()
    return 'Successful Delete!'

@app.post("/list")
def create_list(recipe_ids: list[int], budget: float):
    with Session(engine) as session:
        # Create variables to return
        totalprice = 0
        budgetmessage = ''
        # Dictionary we're returning
        results = {}
        # Select all recipes, looping through to grab total price
        recipes = session.exec(select(Recipe).where(Recipe.id.in_(recipe_ids))).all()
        for recipe in recipes:
            for ingredient in recipe.ingredients:
                # If ingredient not already on the board we add it to price, and the board
                if ingredient.name not in results:
                    results[ingredient.name] = ingredient.price
                    totalprice += ingredient.price
        results['Total Price'] = totalprice
        # Create budget message
        if totalprice <= budget:
            budgetmessage = 'You fit the budget!'
        else:
            missing = totalprice - budget
            budgetmessage = f'You are missing the budget by ${missing:.2f}'
        results['Budget Message'] = budgetmessage
        return results


