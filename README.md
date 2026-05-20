# URL Shortener — Learning FastAPI

A simple URL shortener built with Python and FastAPI. The main goal of this project is to accept a long URL from the user and respond with a shorter, cleaner version that redirects to the original.

---

## Why I Built This

This project was my first step into backend development. I had never worked with fastAPI before, even though I know Python. I chose FastAPI because it is Python-native and beginner-friendly.

---

## What I Learned

### Environment Setup

Before anything else, I learned that installing libraries directly into the system Python environment on a Mac can cause version conflicts down the line. So I created a virtual environment and installed everything there — a habit worth keeping from the start.

### HTTP Protocols — GET and POST

APIs communicate through HTTP protocols. The core idea is simple: a client requests something and a server responds. The two main methods I used are:

- **GET** — used for reading or fetching data. The client is asking *"give me something."*
- **POST** — used for sending data to be processed or stored. The client is saying *"here, take this."*

JSON is the standard data format used for both requests and responses.

### How FastAPI Works

```python
app = FastAPI()
```

This is the line where the application starts. Everything else is built on top of this instance.

Routes are defined using decorators:

```python
@app.get("/")          # handles requests to the root path
@app.get("/user/{username}")  # dynamic path — {username} is a variable
```

Each path has its own job. The decorators tell FastAPI which function to run when a specific path is visited with a specific HTTP method.

### Pydantic Models

Pydantic allows you to define the shape of your data using Python classes that inherit from `BaseModel`. Unlike plain Python classes, Pydantic gives you:

- **Automatic validation** — if the wrong type is sent, it is rejected with a clear error message
- **Automatic parsing** — incoming JSON is converted directly into a Python object
- **Default values** — fields can have defaults (e.g. `in_stock: bool = True`)
- **Auto-generated docs** — FastAPI uses your models to build the interactive `/docs` page

```python
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True
```

### Building the URL Shortener

The core logic is straightforward:

1. User sends a long URL via POST request
2. A random short code (e.g. `aB3xYz`) is generated using Python's `random` and `string` modules
3. The mapping is stored: `short_code → original_url`
4. The short URL is returned to the user

For storage, I used a plain Python dictionary (`db = {}`). It resets every time the server restarts, which is fine for a learning project. A real application would use a proper database.

I used two Pydantic models — one for the input (the long URL the user sends) and one for the output (the short code, short URL, and original URL returned to the user).

### Redirecting

When a user visits a short URL like `http://localhost:8000/aB3xYz`, FastAPI looks up the code in the dictionary and returns a `RedirectResponse`. This is an HTTP 302 response that instructs the browser to navigate to the original URL automatically.

One important lesson: **define specific routes before dynamic ones.** If the dynamic `/{short_code}` route is defined first, FastAPI might treat a path like `/debug/db` as a short code and try to look it up in the dictionary — causing an unexpected error.

### Error Handling

Without error handling, visiting a short code that does not exist causes a `KeyError` and the server returns a 500 error. To handle this properly, I used FastAPI's `HTTPException`:

```python
if short_code not in db:
    raise HTTPException(status_code=404, detail="Short code not found")
```

Common HTTP status codes:

| Code | Meaning |
|---|---|
| 200 | OK — success |
| 201 | Created — something was created |
| 400 | Bad Request — invalid data from the client |
| 404 | Not Found — the resource does not exist |
| 500 | Server Error — something went wrong on the server |

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/your-username/url-shortener.git
cd url-shortener

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn

# Start the server
uvicorn main:app --reload
```

Then open your browser and go to:

- `http://localhost:8000/docs` — interactive API documentation (try the endpoints here)
- `http://localhost:8000/debug/db` — see all stored short codes

---

## Project Structure

```
url_shortener/
└── main.py
```

---

## Example Usage

**Shorten a URL** — send a POST request to `/shorten`:

```json
{
  "url": "https://www.wikipedia.org"
}
```

**Response:**

```json
{
  "short_code": "kT7mNx",
  "short_url": "http://localhost:8000/kT7mNx",
  "original_url": "https://www.wikipedia.org"
}
```

**Redirect** — visit `http://localhost:8000/kT7mNx` in your browser and you will be taken to Wikipedia automatically.

---

## What I Would Add Next

- A real database (SQLite with SQLAlchemy, or PostgreSQL)
- URL validation to reject invalid URLs
- Click tracking — count how many times each short code is visited
- Expiry — short codes that expire after a set time
- A simple frontend

---

## Built With

- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
