from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import string
from fastapi.responses import RedirectResponse # For redirecting to original URL when short URL is accessed

app = FastAPI()

# Our database for now. Lives in memory
db = {}

# Input model, what we expect from the user
class URLInput(BaseModel):
    url: str 
# Output model, what we send back
class URLOutput(BaseModel):
    short_code: str
    short_url: str
    original_url: str

def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits #a-z, A-Z, 0-9
    return "".join(random.choices(characters, k=length))

@app.get("/")
def home():
    return {"message": "Welcome to URL Shortener"}


@app.post("/shorten", response_model=URLOutput)
def shorten_url(data: URLInput):
    # Keep generating untill we get a code that isn't already taken
    short_code = generate_short_code()
    while short_code in db:
        short_code = generate_short_code()

    db[short_code] = data.url

    return URLOutput(
        short_code=short_code,
        short_url=f"http://localhost:8000/{short_code}",
        original_url=data.url
    )

@app.get("/{short_code}")
def redirect(short_code: str):
    if short_code not in db:
        #to indicate that the requested resource was not found
        raise HTTPException(status_code=404, detail=f"Short code '{short_code}' not found")
    original_url = db[short_code]
    return RedirectResponse(url=original_url)

@app.get("/debug/db")
def see_db():
    return db


# @app.post("/items/")
# def create_item(item: Item):
#     return {
#         "received": item,
#         "message": f"Item '{item.name}' costs ${item.price}"
#     }

# @app.get("/about")
# def about():
#     return {"app": "URL Shortener", "version": 1.0}

# @app.get("/user/{username}")
# def get_user(username: str):
#     return {"username": username, "message": f"Hello {username}!"}

# @app.get("/add/{a}/{b}")
# def add(a: int, b: int):
#     return {"a": a, "b": b, "result": a + b}

