from fastapi import FastAPI
from sqlmodel import SQLModel, Field, Session, create_engine, select

app = FastAPI()
# Creates table for Ingredients
class Ingredient(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)
def seed():
    with Session(engine) as session:
        # 13 oz sausage
        session.add(Ingredient(name="Sausage", price= 4))
        # 12 ct eggs
        session.add(Ingredient(name="Eggs", price=2))
        # Barillas
        session.add(Ingredient(name="Rigatoni", price=1.89))
        # smallest possible
        session.add(Ingredient(name="Minced Garlic", price=2))
        session.add(Ingredient(name="Heavy Cream", price=2.96))
        # bagged
        session.add(Ingredient(name="Parmesan Cheese", price=2))
        session.commit()
seed()

@app.get("/")
async def root():
    return {"Hello World"}

@app.get("/ingredients")
def get_ingredients():
    with Session(engine) as session:
        ingredients = session.exec(select(Ingredient)).all()
        return ingredients 

