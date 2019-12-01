# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:01:13 2019

@author: datacore
"""

from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_restful import Resource
import pandas as pd
import os
from azureml.core.workspace import Workspace
from azureml.core.dataset import Dataset

app = Flask(__name__)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
@app.route('/api/WS_create', methods=['POST'])
def WSCreate():
        subscription_id = request.json['subscription_id']
        resource_group = request.json['resource_group']
        workspace_name = request.json['workspace_name']
        location = request.json['location']
        
       ##Existing \ new workspace
        try:
            ws = Workspace(subscription_id=subscription_id,
                                  resource_group=resource_group,
                                  workspace_name=workspace_name)
                                  
            
            print("Found workspace {} at location {}".format(ws.name, ws.location))
            print('Found existing Workspace.')
            return "existing Workspace"
        except:
            print('need to create new Workspace.')
            print('Creating new Workspace.')   
            ws = Workspace.create(name=workspace_name,
                               subscription_id=subscription_id,
                               resource_group=resource_group,
                               #create_resource_group=True,
                               location=location)
            return "ok"
 
@app.route('/api/WS_exist', methods=['POST'])
def WSExist():
        subscription_id = request.json['subscription_id']
        resource_group = request.json['resource_group']
        workspace_name = request.json['workspace_name']
        location = request.json['location']
        
       ##Existing \ new workspace
        try:
            ws = Workspace(subscription_id=subscription_id,
                                  resource_group=resource_group,
                                  workspace_name=workspace_name)
                                  
            
            print("Found workspace {} at location {}".format(ws.name, ws.location))
            print('Found existing Workspace.')
            return "Workspace exist"
        except:
            print('need to create new Workspace.')
            return "Workspace not exist. Please create new workspace."
            
@app.route('/api/upload_data', methods=['POST'])
def UploadCSV():
        subscription_id = request.json['subscription_id']
        resource_group = request.json['resource_group']
        workspace_name = request.json['workspace_name']
        #location = request.json['location']
    
        ws = Workspace(subscription_id=subscription_id,
                                  resource_group=resource_group,
                                  workspace_name=workspace_name)
                                            
        print("Found workspace {} at location {}".format(ws.name, ws.location))
        print('Found existing Workspace.')
        
        ds = ws.get_default_datastore()
        print(ds.datastore_type, ds.account_name, ds.container_name)
        file_path = request.json['file_path']
        print(file_path)
        file_name = request.json['file_name']
        ds.upload(src_dir=file_path, target_path= None, overwrite=True, show_progress=True)
        try:
            stock_ds = Dataset.Tabular.from_delimited_files(path=ds.path(file_name))
            stock_ds = stock_ds.register(workspace = ws,
                                     name = file_name,
                                     description = 'stock training data')
            print('Found existing file name')
            return "This file name exist. Please rename or upload new file"
        except:
            print('Uploading new file, please wait')
            return "new file uploaded"
        
if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=5000)