import os
import random
import sqlite3
import string

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

# Settings come from environment variables, with defaults for local runs
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
DB_PATH = os.getenv("DB_PATH", "urls.db")

app = FastAPI()


# Open a connection to the SQLite database file
def get_conn():
    return sqlite3.connect(DB_PATH)


# Create the table on first run if it does not exist yet
def init_db():
    with get_conn() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS urls (code TEXT PRIMARY KEY, url TEXT NOT NULL)"
        )


init_db()


# What the user sends to /shorten
class URLInput(BaseModel):
    url: str


# What we send back
class URLOutput(BaseModel):
    short_code: str
    short_url: str
    original_url: str


# Make a random code like "aB3xYz"
def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))


@app.get("/")
def home():
    return {"message": "Welcome to URL Shortener"}


# Health check, must stay above /{short_code} or it will be treated as a code
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/shorten", response_model=URLOutput)
def shorten_url(data: URLInput):
    conn = get_conn()
    try:
        while True:
            code = generate_short_code()
            try:
                # Save the code and URL
                with conn:
                    conn.execute("INSERT INTO urls (code, url) VALUES (?, ?)", (code, data.url))
                break
            except sqlite3.IntegrityError:
                continue  # code already taken, try another one
    finally:
        conn.close()  # always close the connection

    return URLOutput(
        short_code=code,
        short_url=f"{BASE_URL}/{code}",
        original_url=data.url,
    )


# Look up the code and redirect to the original URL
@app.get("/{short_code}")
def redirect(short_code: str):
    conn = get_conn()
    try:
        row = conn.execute("SELECT url FROM urls WHERE code = ?", (short_code,)).fetchone()
    finally:
        conn.close()
    # No row means the code does not exist
    if row is None:
        raise HTTPException(status_code=404, detail=f"Short code '{short_code}' not found")
    return RedirectResponse(url=row[0])