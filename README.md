# URL Shortener (FastAPI)
Build: `docker build -t urlshort:1.0 .` #Create an image
Run: `docker run -d --name urlshort -p 8000:8000 -v urlshort-data:/data urlshort:1.0` #Containerize the image with volume
Test: `curl http://localhost:8000/health` #Check the health endpoint
Stop: `docker rm -f urlshort` #Delete the container