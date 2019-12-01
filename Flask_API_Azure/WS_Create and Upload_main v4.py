# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:01:13 2019

@author: datacore
"""

from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_restful import Resource
import pandas as pd
import os
import json
from azureml.core.workspace import Workspace

from azureml.core.dataset import Dataset
from azureml.train.automl import AutoMLConfig
from azureml.core.experiment import Experiment
import logging

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
            #return "This file name exist. Please rename or upload new file"
        except:
            print('Uploading new file, please wait')
        return "new file uploaded"
@app.route('/api/AutoMLRun_Azure', methods=['POST'])
def RunAutoML():
        subscription_id = request.json['subscription_id']
        resource_group = request.json['resource_group']
        workspace_name = request.json['workspace_name']
        file_name = request.json['file_name']
        #location = request.json['location']
    
        ws = Workspace(subscription_id=subscription_id,
                                  resource_group=resource_group,
                                  workspace_name=workspace_name)
                                            
        print("Found workspace {} at location {}".format(ws.name, ws.location))
        print('Found existing Workspace.')
            
        dataset_name = file_name

        # Get a dataset by name
        df = Dataset.get_by_name(workspace=ws, name=dataset_name)
        stock_dataset_df = df.to_pandas_dataframe()
        print('file successfully recieved.')
        stock_dataset_df.head()
        #stock_dataset_json = stock_dataset_df.to_json(orient='split')
        #print(stock_dataset_json)
        y_df = stock_dataset_df['ActionTaken'].values
        x_df = stock_dataset_df.drop(['ActionTaken'], axis=1)
        print(y_df)
        ExperimentName = request.json['ExperimentName']       
        tasks = request.json['tasks']
        iterations = request.json['iterations']
        n_cross_validations = request.json['n_cross_validations']
        iteration_timeout_minutes = request.json['iteration_timeout_minutes']
        primary_metric = request.json['primary_metric']
        max_concurrent_iterations = request.json['max_concurrent_iterations']
        
        #n_cross_validations = request.json['n_cross_validations']
        
        try:
            automl_settings = {
                "name": ExperimentName,
                "iteration_timeout_minutes": iteration_timeout_minutes,
                "iterations": iterations,
                "n_cross_validations": n_cross_validations,
                "primary_metric": primary_metric,
                "preprocess": True,
                "max_concurrent_iterations": max_concurrent_iterations,
                "verbosity": logging.INFO
            }

            automl_config = AutoMLConfig(task=tasks,
                                         debug_log='automl_errors.log',
                                         path=os.getcwd(),
                                         #compute_target = 'Automlvm',
                                         X=x_df,
                                         y=y_df,
                                         **automl_settings,
                                        )

            experiment=Experiment(ws, 'automl_local_v2')
            remote_run = experiment.submit(automl_config, show_output=True)
            remote_run

            return 'ok'
        except:

            return 'error'
            
        
if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=5000)