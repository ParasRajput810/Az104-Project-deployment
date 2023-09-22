#!/bin/sh
sudo ufw allow 5000/tcp
sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip
python3 -m pip install -U pip
sudo pip3 install azure-storage-blob azure-storage-file-share azure-storage-file-datalake azure-storage-queue
pip3 install configparser
sudo pip3 install flask
