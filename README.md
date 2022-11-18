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
git clone git@github.com:harshalkhodifad/AlgoTrading.git
cd AlgoTrading
python3 -m venv venv
source venv/bin/activate
pip3 install --upgrade pip
pip install -r requirements.txt
deactivate
source venv/bin/activate
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
Follow to setup timezone on instance: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/set-time.html

## Login:
```commandline
ssh -i ~/Downloads/AlgoTrading.pem ubuntu@65.0.106.209
```

## Data transfer: 
Reference - https://www.hostinger.in/tutorials/how-to-use-rsync
```commandline
rsync -avhzrP -e "ssh -i ~/Downloads/AlgoTrading.pem" ubuntu@65.0.106.209:~/AlgoTrading/resources/eq_data/ ~/Desktop/Projects/AlgoTrading/resources/eq_data/
rsync -avhzrP -e "ssh -i ~/Downloads/AlgoTrading.pem" ubuntu@65.0.106.209:~/AlgoTrading/algo-trading-* ~/Desktop/Projects/AlgoTrading/
```

## Logic

1. Fetch F&O list
2. Interaction with live data
3. Order placement interaction => (Dummy + Actual)
4. Output order history - unique order id + event type (Print) => Every 5 seconds print whole trades open/closed + Generate PnL by every order
5. Algo logic - strategy -> 



1. Fetch F&O
   - get_fno_list() -> ['A', 'B']
   - get_equity_data('A', 540.6*(1.0075), 540*(1-0.0075))=> round() => 2022-10-27, Closest CE strike price, CE's close, Closest PE Strike price, PE's close

  NFO,ADANIPORTS,60563,OPTSTK,2022-10-27,CE,780.0,1250.0,ADANIPORTS22OCT780CE
  NFO,ADANIPORTS,60564,OPTSTK,2022-10-27,PE,780.0,1250.0,ADANIPORTS22OCT780PE

from io import BytesIO
from zipfile import ZipFile
from urllib.request import urlopen
# or: requests.get(url).content

url = "https://archives.nseindia.com/content/historical/DERIVATIVES/2022/SEP/fo30SEP2022bhav.csv.zip"
file = "fo30SEP2022bhav.csv"

resp = urlopen(url)
myzip = ZipFile(BytesIO(resp.read()))
csv = []
for line in myzip.open(file).readlines():
    csv.append(line.decode('utf-8'))

x = list(filter(lambda y: y.split(',')[4]=='CE' and y.split(',')[1]=='NIFTY' and y.split(',')[2]=='01-Dec-2022', csv))
closest_value(map(lambda y: float(y.split(',')[3]), x), 19030)

def closest_value(input_list, input_value):
  difference = lambda input_list : abs(input_list - input_value)
  res = min(input_list, key=difference)
  return res
2. 






--------------------------------------------


Aarti industries: 745.20
 +0.75%  => 750.789 => round(0.05) => 750.80 
 => 750 Strike price for CE => Previous Close price: 28.05 => *(1.095) => 30.71475 => 30.70 => (30.55(Entry trigger) - 30.7, 30.7 - 30.85(Entry trigger)) => (30.6, 30.8) => SL: 29.15(5%) + 0.5% => 29.30 (SL Trigger)

TARGET 1 - 16% TARGET 2 - 24% AND TARGET 3 - 35% FROM ENTRY PRICE - FOR ALL Entry types.
 
 -- REGULAR ENTRY only if option price stays above previous close.
 
 Example: [Targets: , T1: 35.60, T2: ]
 1. E: 30.7, Max SL: 29.15 => 
 Set trailing SL only after T1.
 
 30.7 -> 35.6 + 1% = 35.95 => 35.6 SL
 
 Set target 2 + 1% tolerance when price is target 1 + 5%.
 
 Don't set target or sl in broker.
 
 Set SL when (30.7 - 29.15) = 1.55*0.4 = 0.62 => 0.6 => (30.7-0.6) => 30.1 => Put SL order.
 
 
 
 -- REVISED 1:
 Option price stays above -18% from previous close - 28.05 => 23.
 Entry price: +10% current day low (i.e. 24 current day low => 26.4 + tolerance => SL(5%) => Targets as mentioned above)
 
  -- REVISED 2:
   Option price breaks -18% from previous close - 28.05 => 23.
 Entry price: +12% current day low (i.e. 20 current day low => 22.4 + tolerance => SL(5%) => Targets as mentioned above)


Trailing stoploss: [After crossing target 3]
 
 Tolerance: 0.5%
 
 - Fetch data one day earlier rather than in morning.