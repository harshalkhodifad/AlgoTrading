# AlgoTrading

## Setup Instructions:
```commandline
ssh-keygen
cat ~/.ssh/id_rsa.pub -> Add this to github allowed keys
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3.7
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
sudo update-alternatives --config python3
sudo apt install python3-pip
pip3 install --upgrade pip
sudo apt-get install python3.7-venv
<Paste AlgoTrading folder>
cd AlgoTrading
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt
deactivate
source venv/bin/activate
# python3 main.py
```

## Cron Setup: https://www.digitalocean.com/community/tutorials/how-to-use-cron-to-automate-tasks-ubuntu-1804
minute hour day_of_month month day_of_week command_to_run
```commandline
sudo apt install cron
sudo systemctl enable cron
run_algo - command name: /bin/run_algo -> chmod +x run_algo

cd /home/ubuntu/AlgoTrading
source venv/bin/activate
nohup /home/ubuntu/AlgoTrading/venv/bin/python3 main.py &

crontab -e
# minute hour day_of_month month day_of_week(0 to 6 - 0=Sunday) command
0 8 * * 1-5 run_algo

service cron status
service cron stop
sudo pkill -u root python
sudo pgrep -u root python
ps -Af | grep python
```

## Permissions setup shared with root
Reference: https://superuser.com/questions/19318/how-can-i-give-write-access-of-a-folder-to-all-users-in-linux
```commandline
sudo groupadd root_users
sudo usermod -a -G root_users ubuntu
sudo usermod -a -G root_users root
sudo chgrp -R root_users AlgoTrading/
sudo chmod -R g+w AlgoTrading/
sudo find AlgoTrading/ -type d -exec chmod 2775 {} \;
sudo find AlgoTrading/ -type f -exec chmod ug+rw {} \;
# <logout & login>
```

## EC2 Setup:
Follow to setup timezone on instance to IST: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html

## Login:
```commandline
ssh -i ~/Downloads/AlgoTrading.pem ubuntu@65.0.106.209
```

## Data transfer: 
Reference - https://www.hostinger.in/tutorials/how-to-use-rsync
```commandline
rsync -avhzrP -e "ssh -i ~/Downloads/AlgoTrading.pem" ubuntu@65.0.106.209:~/AlgoTrading/logs/algo-trading-* ~/Desktop/Projects/AlgoTrading/logs/
```
