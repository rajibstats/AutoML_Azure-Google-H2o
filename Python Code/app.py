# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 10:32:27 2019

@author: datacore
"""

from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import pickle as p
import json
#import automl
import azureml.train.automl

app = Flask(__name__)


@app.route('/api/', methods=['POST'])
def makecalc():
    #data = request.get_json()
    data = request.get_json()
    prediction = np.array2string(model.predict(data))

    return jsonify(prediction)

if __name__ == '__main__':
    modelfile = 'D:\\Stock_Prediction\\AutoML_Azure\\new_model2.pkl'
    model = p.load(open(modelfile, 'rb'))
    app.run(debug=True, host='127.0.0.1',port = 5000)
    
    