#!/usr/bin/env python
# coding: utf-8

# In[1]:
import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient
import string
import random
import requests
import configparser

app = Flask(__name__, instance_relative_config=True)

Config = configparser.ConfigParser()
Config.read("config.py")

# Account name
account = Config.get('DEFAULT', 'account')
# Azure Storage account access key
key = Config.get('DEFAULT', 'key')
# Container name
container = Config.get('DEFAULT', 'container')


# blob_service = BlockBlobService(account_name=account, account_key=key)

blob_service_client = BlobServiceClient(account_url=f'https://{account}.blob.core.windows.net/', credential=key)

@app.route("/")
def main():
    return render_template('index.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            try:
                # Generate a random filename
                random_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                filename = secure_filename(file.filename)
                fileextension = filename.rsplit('.', 1)[1]
                unique_filename = f"{random_filename}.{fileextension}"

                # Upload the file to Azure Storage container
                blob_service_client.get_blob_client(container=container, blob=unique_filename).upload_blob(file)

                # Construct the URL to the uploaded file
                uploaded_file_url = f'https://{account}.blob.core.windows.net/{container}/{unique_filename}'
                return f"File uploaded successfully. URL: {uploaded_file_url}"
            except Exception as e:
                return f"An error occurred: {str(e)}"

    return render_template('uploadfile.html')

@app.route("/home" , methods=['GET'])
def homepage():
    return render_template('homepage.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
