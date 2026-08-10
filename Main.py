from fastapi import FastAPI
from sqlmodel import SQLModel, Field, Session, create_engine, select, Relationship
from sqlalchemy.orm import selectinload
# Creates web app object
app = FastAPI()
# Creates table for Recipe to Ingredient link, inherits sql model
class RecipeIngredient(SQLModel, table=True):
    recipe_id: int = Field(foreign_key="recipe.id", primary_key=True)
    ingredient_id: int = Field(foreign_key="ingredient.id", primary_key=True)
# Ingredient Table
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

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)


def seed():
    with Session(engine) as session:
        # Clears the database for now
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

@app.on_event("startup")
def on_startup():
    seed()
@app.get("/")
async def root():
    return {"Hello World"}

@app.get("/ingredients")
def get_ingredients():
    with Session(engine) as session:
        # returns whole ingredient database
        ingredients = session.exec(select(Ingredient)).all()
        return ingredients 

@app.get("/recipes")
def get_recipes():
    with Session(engine) as session:
        #loads in recipes from database
        recipes = session.exec(select(Recipe)).all()
        #holds result for ingredients to fill
        result = []
        # for loop to append formatted data from each recipe to result
        for recipe in recipes:
            ingredients = session.exec(
                select(Ingredient)
                .join(RecipeIngredient)
                .where(RecipeIngredient.recipe_id == recipe.id)
            ).all()
        # formatting for current recipe
            result.append({
                "id": recipe.id,
                "name": recipe.name,
                "owner": recipe.owner,
                "ingredients": ingredients
            })
        
        return result

