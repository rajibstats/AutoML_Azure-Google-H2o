# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 16:46:15 2019

@author: datacore
"""
import logging

from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets
from azureml.core import Workspace

import azureml.core
from azureml.core.experiment import Experiment
from azureml.core.workspace import Workspace
from azureml.train.automl import AutoMLConfig


# inputs for workspace creation
#myworkspace = input("Enter your workspace name : ")
myworkspace = 'automldemo'
#subscription_id = input("Enter your azure-subscription : ")
subscription_id = 'b613a36c-3018-4806-9e67-2af6fc80b3b3' 
#myresourcegroup = input("Enter your resourcegroup name : ")
myresourcegroup = 'PMGDemo'
#location = input("Enter your location name : ")
location = 'southcentralus'

##Existing \ new workspace
try:
    ws = Workspace(subscription_id="b613a36c-3018-4806-9e67-2af6fc80b3b3",
                   resource_group="PMGDemo",
                   workspace_name="automldemo")
    
    print("Found workspace {} at location {}".format(ws.name, ws.location))
    print('Found existing Workspace.')
    
except:
    print('need to create new Workspace.')
    print('Creating new Workspace.')
    
    ws = Workspace.create(name=myworkspace,
                      subscription_id=subscription_id,
                      resource_group=myresourcegroup,
                      #create_resource_group=True,
                      location=location)