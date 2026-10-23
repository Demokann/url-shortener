import os
import random
import string
import time

import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

# Settings come from environment variables
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "urlshort")
DB_USER = os.getenv("DB_USER", "urlshort")
DB_PASSWORD = os.environ["DB_PASSWORD"]  # no default on purpose: fail fast if missing

app = FastAPI()


# Open a new connection to PostgreSQL (the host is the Compose service name)
def get_conn():
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


# Create the table if it does not exist yet, retrying while the database wakes up
def init_db(retries: int = 10, delay: float = 1.0):
    for attempt in range(retries):
        try:
            with get_conn() as conn:
                conn.execute(
                    "CREATE TABLE IF NOT EXISTS urls (code TEXT PRIMARY KEY, url TEXT NOT NULL)"
                )
            return
        except psycopg.OperationalError:
            if attempt == retries - 1:
                raise
            time.sleep(delay)


init_db()


class URLInput(BaseModel):
    url: str


class URLOutput(BaseModel):
    short_code: str
    short_url: str
    original_url: str


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
    # "with" commits on success and closes the connection at the end
    with get_conn() as conn:
        while True:
            code = generate_short_code()
            # DO NOTHING on a duplicate code, rowcount 0 means "taken, try another"
            cur = conn.execute(
                "INSERT INTO urls (code, url) VALUES (%s, %s) ON CONFLICT (code) DO NOTHING",
                (code, data.url),
            )
            if cur.rowcount == 1:
                break

    return URLOutput(
        short_code=code,
        short_url=f"{BASE_URL}/{code}",
        original_url=data.url,
    )


@app.get("/{short_code}")
def redirect(short_code: str):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT url FROM urls WHERE code = %s", (short_code,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Short code '{short_code}' not found")
    return RedirectResponse(url=row[0])