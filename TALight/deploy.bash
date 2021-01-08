sudo apt-get install docker-compose -y
sudo docker-compose down
sudo docker system prune -a
sudo docker-compose up -d --build
