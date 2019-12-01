# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 17:07:45 2019

@author: datacore
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:01:13 2019

@author: datacore
"""

from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_restful import Resource
import os
import pandas as pd
import h2o
from h2o.automl import H2OAutoML

app = Flask(__name__)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

@app.route('/api/WS_create_h2o', methods=['POST'])
def WSCreate():
        ip = request.json['ip']
        port  = request.json['port']
        nthreads  = request.json['nthreads']
        max_mem_size = request.json['max_mem_size']
        
       ##Existing \ new workspace
        nthreads = int(nthreads)
        ws = h2o.init(ip = ip, port = port , nthreads = nthreads, max_mem_size = max_mem_size )
        print('Found existing Workspace.')
        print(type(nthreads))
        return "existing Workspace"
        
        
@app.route('/api/upload_data_h2o', methods=['POST'])
def UploadCSV():
        file = request.json['file_path']
        print(file)
        data = h2o.import_file(file)
        #des_data = data.describe()
        print(data)
        return "file uploaded successfully" 
    
@app.route('/api/AutoMLRun_h2o', methods=['POST'])

def RunAutoML():   
        file = request.json['file_path']
        max_models = request.json['max_models']
        max_runtime_secs  = request.json['max_runtime_secs']
        seed  = request.json['seed']
        ip = request.json['ip']
        port  = request.json['port']
        nthreads  = request.json['nthreads']
        max_mem_size = request.json['max_mem_size']
        target_var = request.json['target_var']
       ##Existing \ new workspace
        h2o.init(ip = ip, port = port , nthreads = nthreads, max_mem_size = max_mem_size )
        print('Found existing Workspace.')
        data = h2o.import_file(file)
        predictors = list(data.columns) 
        predictors.remove(target_var)  # Since we need to predict quality
        print(predictors)
        aml = H2OAutoML(max_models = max_models, max_runtime_secs=max_runtime_secs, seed = seed)
        aml.train(x=predictors, y=target_var, training_frame=data)
        #print(aml.leaderboard)
        aml_lb = aml.leaderboard
        print(aml_lb)
        dff = aml_lb.as_data_frame()
        print(dff)
        # changing index cols with rename() 
        dff.rename(index = {0: "one", 1: "two",2: "three",3: "four",4: "five"}, 
                                 inplace = True) 
        dff_json = dff.to_json(orient='index')
        print(dff_json)
        best_model_name = aml.leader.model_id
        best_model_name
        var1 = "@"
        var3 = var1 + best_model_name
        var3
        return  '{} {}'.format(dff_json, var3)
        #return dff_json

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=54321)