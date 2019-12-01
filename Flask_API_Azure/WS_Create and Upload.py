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
        
@app.route('/api/upload_data', methods=['POST'])
def UploadCSV():
        file = request.json['file_path']
        print(file)
        data = pd.read_csv(file)
        print(data)
        return "ok"
        
if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=5000)