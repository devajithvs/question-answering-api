docker rm --force bb ; git pull ; docker build --tag test:1.0 .; docker run --publish 8080:8080 --name bb test:1.0
docker rm --force bb; docker rmi $(docker images -q) --force