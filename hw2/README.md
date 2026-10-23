cp .env.example .env
docker compose up -d --build && sleep 8
CODE=$(curl -s -X POST localhost:8000/shorten -H "Content-Type: application/json" -d '{"url":"https://example.com"}' | sed -E 's/.*"short_code":"([^"]+)".*/\1/')
curl -i localhost:8000/$CODE
docker compose down