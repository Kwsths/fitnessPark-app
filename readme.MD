init a docker image with name calendar-app
docker build -t calendar-app .
run the app and reroute the port 5000 of docker image on 5000 f this machine
with -w we declare the current working directory of the container
with the -v we are linking our directory with docker directory
docker run -d -p 5000:5000  -w /app -v "$(pwd):/app" calendar-app