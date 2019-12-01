# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 10:25:01 2019

@author: datacore
"""
#Required packages
from azureml.core import Workspace
import azureml.core 
from azureml.core.compute import AmlCompute
from azureml.core.authentication import AzureCliAuthentication
import azure.cli.core

##### Authentication with Azure

#cli_auth = AzureCliAuthentication()
#ws = Workspace.from_config()

# inputs for workspace creation
#myworkspace = input("Enter your workspace name : ")
myworkspace = 'automldemo1'
#subscription_id = input("Enter your azure-subscription : ")
subscription_id = '24075937-2687-4457-bac6-ec16dec514c3' 
#myresourcegroup = input("Enter your resourcegroup name : ")
myresourcegroup = 'PMGDemo1'
#location = input("Enter your location name : ")
location = 'southcentralus'

#Inputs for VM creation
#vm_size = input("Enter your vm_size : ")
#min_nodes = input("Enter your min_nodes : ")
#max_nodes = input("Enter your max_nodes : ")

#Inputs for VM creation
vm_size = "Standard_D2_v2"
min_nodes = 1
max_nodes = 4

##Existing \ new workspace
try:
    ws = Workspace(subscription_id="24075937-2687-4457-bac6-ec16dec514c3",
                   resource_group="PMGDemo",
                   workspace_name="AutoML_demo1")
    
    print("Found workspace {} at location {}".format(ws.name, ws.location))
    print('Found existing Workspace.')
    
except:
    print('need to create new Workspace.')
    print('Creating new Workspace.')
    
    ws = Workspace.create(name=myworkspace,
                      subscription_id=subscription_id,
                      resource_group=myresourcegroup,
                      create_resource_group=True,
                      location=location)
    
#Checking chuster available or create new cluster
aml_name = 'cpu-cluster'
try:
    aml_compute = AmlCompute(ws, aml_name)
    print('Found existing AML compute context.')
except:
    print('Creating new AML compute context.')
    aml_config = AmlCompute.provisioning_configuration(vm_size = vm_size, min_nodes= min_nodes, max_nodes= max_nodes)
    aml_compute = AmlCompute.create(ws, name = aml_name, provisioning_configuration = aml_config)
    aml_compute.wait_for_completion(show_output = True)


#list of experiment with you have created in your workspace
from azureml.core.experiment import Experiment    
list_experiments = Experiment.list(ws)    
list_experiments

import azurerm
token = azurerm.get_access_token_from_cli()
azurerm.list_subscriptions(token)  

#Delete full workspace
ws.delete(delete_dependent_resources=True, no_wait=False)

##Delete your computor cluster
aml_compute.delete()




   
