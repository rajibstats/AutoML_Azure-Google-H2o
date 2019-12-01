# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 17:39:14 2019

@author: datacore
"""
from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_restful import Resource
import pandas as pd
import os
import json

app = Flask(__name__)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
@app.route('/api/upload_data', methods=['POST'])
def UploadCSV():
        file = request.json['file_path']
        print(file)
        data = pd.read_csv(file)
        print(data)
        return "ok"
        
if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=5000)
    
    
    

