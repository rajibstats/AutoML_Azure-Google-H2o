# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 12:48:45 2019

@author: datacore
"""
from azureml.core.workspace import Workspace

#cli_auth = AzureCliAuthentication()
ws = Workspace(subscription_id="b613a36c-3018-4806-9e67-2af6fc80b3b3",
               resource_group="PMGDemo",
               workspace_name="AutoML_demo")

print("Found workspace {} at location {}".format(ws.name, ws.location))


from azureml.core.compute import AmlCompute
aml_name = 'cpu-cluster1'
try:
    aml_compute = AmlCompute(ws, aml_name)
    print('Found existing AML compute context.')
except:
    print('Creating new AML compute context.')
    vm_size = input("Enter your vm_size : ")
    min_nodes = input("Enter your min_nodes : ")
    max_nodes = input("Enter your max_nodes : ")
    aml_config = AmlCompute.provisioning_configuration(vm_size = vm_size, min_nodes= min_nodes, max_nodes= max_nodes)
    aml_compute = AmlCompute.create(ws, name = aml_name, provisioning_configuration = aml_config)
    aml_compute.wait_for_completion(show_output = True)