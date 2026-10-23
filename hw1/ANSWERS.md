# ANSWERS

## 1. Instruction order

My Dockerfile goes from the least to the most frequently changing instructions: base image, working directory, requirements.txt copy, pip install, user creation, application code copy, and finally the runtime settings and start command. Docker caches every layer and reuses it until an instruction or the files it depends on change, after which all later layers are rebuilt. Because requirements.txt is installed before the source code is copied, a code edit only rebuilds the last layer; in my second build the pip install step showed CACHED and the whole build took 0.8 seconds. If I swapped them and copied all source code before pip install, every code change would invalidate the install layer and download all packages through requirements.txt again, which took about 11 seconds in my first build.

## 2. Data in removed containers

Data written to the container's writable layer is deleted together with the container when it is removed. To keep it, the data must be stored outside the container's own filesystem, using a named volume or a bind mount at the path where the app writes. My app writes its SQLite file to /data/urls.db, and I mount the volume urlshort-data at /data. I tested this: after removing and recreating the container with the volume, an old short link still redirected, and without the volume it returned 404. In general, important state should live in a volume at minimum, or ideally in an external database or storage service, so containers stay disposable and replaceable.

## 3. The latest tag

The latest tag is a moving pointer, so it points to a different image whenever a new version is published. The same Dockerfile can therefore produce different images on different days, and a build that worked yesterday may break today without any change in my code. Instead, I pinned the base image to python:3.14.6-slim-bookworm, which matches the Python version I developed with. I also pinned every Python dependency to an exact version in requirements.txt using pip freeze.

## AI assistant use

I used an AI assistant to help draft the Dockerfile and the changes to main.py (the /health endpoint, environment variables and SQLite storage). I built, ran and tested everything myself, and I rewrote the written answers in my own words.

## Image size note

Running `docker image ls` shows that the final image occupies 231 MB on disk (with a compressed registry download size of 49.5 MB). By selecting `python:3.14.6-slim-bookworm` as the base image, excluding unnecessary local files via `.dockerignore`, and using `--no-cache-dir` during installation, the image footprint was kept smaller than the standard Python base image.
