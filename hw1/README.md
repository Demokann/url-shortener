# URL Shortener (FastAPI)
Build: `docker build -t urlshort:1.0 .` #Build the docker image
Run: `docker run -d --name urlshort -p 8000:8000 -v urlshort-data:/data urlshort:1.0` #Run the container with persistent volume
Test: `curl http://localhost:8000/health` #Test the health endpoint
Stop: `docker rm -f urlshort` #Stop and remove the container