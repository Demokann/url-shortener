# ANSWERS

## 1. Your app calls the second service by name. How does that work, and why does the same name not work between two containers on the default docker run network?

Docker Compose creates a user-defined network for the project (url_shortener_default) and attaches both containers to it. User-defined networks have a built-in DNS server that turns a service name into the current IP address of that container. My app uses DB_HOST=db, so it finds the PostgreSQL container without any IP address in the code. The default network used by plain `docker run` has no such DNS, so containers there can only reach each other by IP, and a name like `db` fails with "bad address". This is also why names are better than IPs: a container can get a different IP after a restart, but its service name stays the same.

## 2. Which of your services is stateless and which is not? Show the evidence: what did you do, and what happened to your data (for example docker compose rm -sf app and then docker compose down, and docker compose down -v)?

The app service is stateless and the db service is stateful. I created one short link and then called it again after each experiment. After `docker compose rm -sf app` and `docker compose up -d`, the link still redirected (307), because the data is in PostgreSQL and not in the app container. After `docker compose down` and `up -d`, it still redirected (307), because `down` removes the containers but keeps the named volume pgdata. After `docker compose down -v`, the same link returned 404, because the volume was deleted together with the database files. The app writes nothing to its own disk, since I removed SQLite, so I can delete and recreate it at any time.

## 3. Where should a database password come from, and why is it a problem to commit it to Git, even in a private repository?

The password should come from the environment at runtime, in my case from a `.env` file that is listed in `.gitignore`, and Compose passes it with `${DB_PASSWORD}`. In the repository I commit only `.env.example` with a fake value. Git keeps the full history, so a password that was committed once stays readable in old commits even if I delete the file later. Everyone with access to the repository, every clone and every fork also gets a copy, and a private repository can become public or be shared by mistake. If a secret leaks, I would also have to change it everywhere.

## AI assistant use

I used an AI assistant to plan the steps, to adapt main.py from SQLite to PostgreSQL, and to help write the Dockerfile and compose.yaml. I built, ran and tested everything myself, including the three state experiments, and I wrote the final answers in my own words.