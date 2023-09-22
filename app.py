#!/usr/bin/env python
# coding: utf-8

import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
import configparser

app = Flask(__name__, instance_relative_config=True)

Config = configparser.ConfigParser()
Config.read("config.ini")

# Account name
account = Config.get('DEFAULT', 'account')
# Azure Storage account access key
key = Config.get('DEFAULT', 'key')
# Container name
container = Config.get('DEFAULT', 'container')

blob_service_client = BlobServiceClient(account_url=f'https://{account}.blob.core.windows.net/', credential=key)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            try:
                blob_service_client.get_blob_client(container=container, blob=filename).upload_blob(file)
                ref = f'https://{account}.blob.core.windows.net/{container}/{filename}'
            except Exception as e:
                print('Exception:', str(e))
                ref = None

    return render_template('uploadfile.html', ref=ref)

@app.route("/home", methods=['GET'])
def homepage():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)


# In[ ]:
