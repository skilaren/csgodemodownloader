sudo apt update
sudo apt install python3
sudo apt install python3-pip
pip3 install -r req.txt
nohup celery -A tasks worker --loglevel=INFO -Ofair -f logs_new.txt -c 30 &