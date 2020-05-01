ls
docker pull mysql:latest
sudo apt-get update
sudo apt-get install     apt-transport-https     ca-certificates     curl     gnupg-agent     software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt install docker.io
docker pull mysql:latest
ls
mkdir ~/cs4501/db
cd cs4501/
ls
docker ps -a
docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$3cureUS' -v ~/cs4501/db:/var/lib/mysql  mysql:latest
docker os -a
docker ps -a
docker run -it --name mysql-cmdline --link mysql:db mysql:latest bash
docker ps -a
docker exec -it mysql-cmdline
docker exec -it mysql-cmdline bash
docker start mysql-cmdline
docker exec -it mysql-cmdline bash
docker network ls
rm -r db/
docker rm mysql
docker stop mysql
docker rm mysql
docker stop mysql-cmdline
docker rm mysql-cmdline
docker ps -a
ls
mkdir ~/cs4501/db
docker run --name mysql -d -e MYSQL_ROOT_PASSWORD='$3cureUS' -v ~/cs4501/db:/var/lib/mysql  mysql:latest
docker run -it --name mysql-cmdline --link mysql:db mysql:latest bash
cd app/
docker-compose start models
apt install docker-compose
docker-compose start models
docker-compose up models
docker network ls
docker network connect app-backend mysql
docker network connect app_backend mysql
docker-compose up models
docker exec -it mysql-cmdline bash
docker start mysql-cmdline
docker exec -it mysql-cmdline bash
docker-compose up models
bg
cd models/
ls
cd api/
ls
cd ..
cd models/
ls
vi settings.py 
cd ..
cd ~/cs4501/app/
cd exp/exp/
vi settings.py 
docker-compose up exp
bg
docker-compose up kafka
bg
cd ../..
cd exp/exp/
vi settings.py 
cd exp/exp/
cd ../..
cd web/
cd frontend/
cd ..
cd web/
vi settings.py 
cd ../..
docker-compose up
bg
cd web/web/
vi settings.py 
cd ..
docker-compose stop
docker-compose up &
jobs
fg 1
fg 2
logout
