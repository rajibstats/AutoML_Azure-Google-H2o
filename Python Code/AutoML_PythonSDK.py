# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 16:06:57 2019

@author: datacore
"""

from azureml.core.workspace import Workspace
import azureml.core
import pandas as pd

from azureml.core.authentication import AzureCliAuthentication
import azure.cli.core

#cli_auth = AzureCliAuthentication()
ws = Workspace(subscription_id="b613a36c-3018-4806-9e67-2af6fc80b3b3",
               resource_group="PMGDemo",
               workspace_name="AutoML_demo")

print("Found workspace {} at location {}".format(ws.name, ws.location))


ws = Workspace.from_config()

# Choose a name for the experiment and specify the project folder.
experiment_name = 'Capstone_Project'
project_folder = 'D:\\Stock_Prediction\\AutoML_Azure\\Python_AutoML'

from azureml.core.experiment import Experiment
experiment = Experiment(ws, experiment_name)

output = {}
output['SDK version'] = azureml.core.VERSION
output['Subscription ID'] = ws.subscription_id
output['Workspace Name'] = ws.name
output['Resource Group'] = ws.resource_group
output['Location'] = ws.location
output['Project Directory'] = project_folder
output['Experiment Name'] = experiment.name
pd.set_option('display.max_colwidth', -1)
outputDf = pd.DataFrame(data = output, index = [''])
outputDf.T


from azureml.core.compute import AmlCompute

aml_name = 'cpu-cluster'
try:
    aml_compute = AmlCompute(ws, aml_name)
    print('Found existing AML compute context.')
except:
    print('Creating new AML compute context.')
    aml_config = AmlCompute.provisioning_configuration(vm_size = "Standard_D2_v2", min_nodes=1, max_nodes=4)
    aml_compute = AmlCompute.create(ws, name = aml_name, provisioning_configuration = aml_config)
    aml_compute.wait_for_completion(show_output = True)
    
    
#writefile get_data.py

from sklearn import datasets
from sklearn.model_selection import train_test_split
from scipy import sparse
import numpy as np

#def get_data():
boston = pd.read_csv('C:\\Users\\datacore\\OneDrive\\Desktop\\Capstone Project\\train_values_wJZrCmI.csv')
X = boston.drop(columns = ['poverty_probability'])
y = boston['poverty_probability']
y=y.to_numpy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

#return {'X': X_train, 'y': y_train}

def get_data():
    boston = datasets.load_boston()
    X = boston.data
    y = boston.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

    return {'X': X_train, 'y': y_train}


import logging
import os
import time
from azureml.train.automl import AutoMLConfig

automl_settings = {
    "name": "AutoML_Demo_Experiment",
    "iteration_timeout_minutes": 15,
    "iterations": 25,
    "n_cross_validations": 5,
    "primary_metric": 'r2_score',
    "preprocess": False,
    "max_concurrent_iterations": 8,
    "verbosity": logging.INFO
}

automl_config = AutoMLConfig(task='regression',
                             debug_log='automl_errors.log',
                             path=os.getcwd(),
                             compute_target = aml_compute,
                             data_script="get_data.py",
                             #X=X_train,
                             #y=y,
                             **automl_settings,
                            )

from azureml.core.experiment import Experiment
experiment=Experiment(ws, 'automl_remote')
remote_run = experiment.submit(automl_config, show_output=True)



