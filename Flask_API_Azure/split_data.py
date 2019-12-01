# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:26:47 2019

@author: datacore
"""

from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_restful import Resource
import pandas as pd
import os
from sklearn import datasets
from sklearn.model_selection import train_test_split

app = Flask(__name__)

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
@app.route('/api/split', methods=['POST'])

def UploadCSV():
        file = request.json['file_path']
        print(file)
        data = pd.read_csv(file)
        print(data)
        return "ok"
    
def get_data():
    boston = datasets.load_boston()
    X = boston.data
    y = boston.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=1)
    print(X_train.shape)
    print(X_train.head())
    return {'X': X_train, 'y': y_train}
        
if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=5000)
