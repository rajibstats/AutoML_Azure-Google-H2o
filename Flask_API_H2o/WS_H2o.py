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
        ws = h2o.init(ip = ip, port = port , nthreads = nthreads, max_mem_size = max_mem_size )
        print('Found existing Workspace.')
        return "existing Workspace"
        return ws

        
@app.route('/api/upload_data_h2o', methods=['POST'])
def UploadCSV():
        file = request.json['file_path']
        print(file)
        data = h2o.import_file(file)
        #print(data)
        return data    

@app.route('/api/split_h20', methods=['POST'])
def SplitCSV():
        file = request.json['file_path']
        print(file)
        data = h2o.import_file(file)
        #print(data)
        stock_split = data.split_frame(ratios = [0.8], seed = 1234)
        stock_train = stock_split[0] # using 80% for training
        stock_test = stock_split[1] #rest 20% for testingprint(wine_train.shape, wine_test.shape)
        print(stock_train.shape, stock_test.shape)
        return stock_train, stock_test


        
if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=54321)