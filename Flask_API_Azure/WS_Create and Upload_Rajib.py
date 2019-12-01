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
from sklearn.model_selection import train_test_split
from azureml.core.experiment import Experiment
from azureml.train.automl import AutoMLConfig
import logging

userData = {}

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
            userData[subscription_id] = [ws]
            return 'Found existing Workspace.'
            
        except:
            print('need to create new Workspace.')
            print('Creating new Workspace.')   
            ws = Workspace.create(name=workspace_name,
                               subscription_id=subscription_id,
                               resource_group=resource_group,
                               #create_resource_group=True,
                               location=location)
            userData[subscription_id] = ws
            return 'Creating new Workspace.'
        
#ws = WSCreate()
        
@app.route('/api/upload_data', methods=['POST'])
def UploadCSV():
        file = request.json['file_path']
        ReadCSV(file)
        return "ok"
    
def ReadCSV(file):
        data = pd.read_csv(file)
        return data   
    
@app.route('/api/split', methods=['POST'])
def SplitCSV():
        file = request.json['file_path']
        subscription_id = request.json['subscription_id']
        data = ReadCSV(file)
        y_df = data['ActionTaken']
        x_df = data.drop(['ActionTaken'], axis=1)
        (X_train, X_test, y_train, y_test) = train_test_split(x_df, y_df,
            test_size=0.2, random_state=42)
        print(X_train.shape)
        print(X_train.head())
        x_df1 = x_df.to_json(orient='split')
        y_df1 = y_df.to_json(orient='split')
        #return {'X': X_train, 'y': y_train}
        userData[subscription_id].append(x_df1)
        userData[subscription_id].append(y_df1)
        return x_df1, y_df1
    
   

@app.route('/api/AutoMLRun', methods=['POST'])

def RunAutoML():   
    automl_settings = {
    "name": "AutoML_Demo_Experiment",
    "iteration_timeout_minutes": 15,
    "iterations": 3,
    "n_cross_validations": 5,
    "primary_metric": 'r2_score',
    "preprocess": False,
    "max_concurrent_iterations": 8,
    "verbosity": logging.INFO
    }
    subscription_id = request.json['subscription_id']
    print(userData)
    print(userData[subscription_id])
    #return "ok"
    try:
        automl_config = AutoMLConfig(task="classification",
                        X=userData[subscription_id][1],
                        y=userData[subscription_id][2],
                        debug_log='automl_errors.log',
                        preprocess=True,
                        **automl_settings,
                        )
        experiment=Experiment(userData[subscription_id][0], 'automl_remote')
        run = experiment.submit(automl_config, show_output=True)
        run
        best_model,fitted_model = run.get_output()

        return 'ok'
    except:
        return 'error'  
      
if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=5000)