# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:25:01 2019

@author: datacore
"""
from azureml.core import Workspace

import azureml.core


from azureml.core.authentication import AzureCliAuthentication
import azure.cli.core
#ws = Workspace.from_config()

##Existing \ new workspace
try:
    ws = Workspace(subscription_id="b613a36c-3018-4806-9e67-2af6fc80b3b3",
                   resource_group="PMGDemo1",
                   workspace_name="AutoML_demo")

    print("Found workspace {} at location {}".format(ws.name, ws.location))
    print('Found existing Workspace.')
    
except:
    print('need to create new Workspace.')
    myworkspace = input("Enter your workspace name : ") 
    subscription_id = input("Enter your azure-subscription : ") 
    myresourcegroup = input("Enter your resourcegroup name : ")
    location = input("Enter your location name : ")
    
    print('Creating new Workspace.')
    
    ws = Workspace.create(name=myworkspace,
                      subscription_id=subscription_id,
                      resource_group=myresourcegroup,
                      create_resource_group=True,
                      location=location
                     )
    
    



    
    
    
    