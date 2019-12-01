# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 14:51:44 2019

@author: datacore
"""
from azureml.core import Workspace
import azureml.core
##### Authentication with Azure
#cli_auth = AzureCliAuthentication()
#ws = Workspace.from_config()

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
    
ws_details = ws.get_details() 
ws_details       

# =============================================================================
# # retrieve an existing datastore in the workspace by name
# datastore = Datastore.get(ws, datastore_name)
# # create a TabularDataset from a delimited file behind a public web url
# web_path ='https://dprepdata.blob.core.windows.net/demo/Titanic.csv'
# titanic_ds1 = Dataset.Tabular.from_delimited_files(path=web_path)
# 
# # preview the first 3 rows of titanic_ds
# titanic_ds1.take(3).to_pandas_dataframe()
# titanic_ds1 = titanic_ds1.register(workspace = ws,
#                                  name = 'titanic_ds1',
#                                  description = 'titanic training data')
# =============================================================================
import json 
import azureml.data
from azureml.data.azure_storage_datastore import AzureFileDatastore, AzureBlobDatastore
ds = ws.get_default_datastore()
print(ds.datastore_type, ds.account_name, ds.container_name)

data_folder = "D:\\Stock_Prediction\\AutoML_Azure\\stocks_data\\stocks_data"
ds.upload(src_dir=data_folder, target_path= None, overwrite=True, show_progress=True)

from azureml.core.dataset import Dataset
stock_dataset = Dataset.Tabular.from_delimited_files(path=ds.path('2018Q4PredictionTrainedSet10.csv'))

# preview the first 3 rows of titanic_ds
#stock_ds.take(3).to_pandas_dataframe()

stock_dataset = stock_dataset.register(workspace = ws,
                                 name = 'stock_dataset',
                                 description = 'stock training data')
###############################################################################

# Get a dataset by name
file_name = 'stock_dataset'
stock_dataset = Dataset.get_by_name(ws, 'stock_dataset')
stock_dataset_df = stock_dataset.to_pandas_dataframe()
y_df = stock_dataset_df['ActionTaken'].values
x_df = stock_dataset_df.drop(['ActionTaken'], axis=1)

###############################################################################        
ExperimentName = "AutoML_Demo_Experiment_from_API"       
tasks = "classification"
iterations = 12
iteration_timeout_minutes = 6
primary_metric = "AUC_weighted"

from azureml.train.automl import AutoMLConfig
from azureml.core.experiment import Experiment        
#n_cross_validations = request.json['n_cross_validations']
automl_config = AutoMLConfig(
                    task=tasks,
                    X=x_df,
                    y=y_df,
                    iterations=iterations,
                    iteration_timeout_minutes=iteration_timeout_minutes,
                    primary_metric=primary_metric,
                    #n_cross_validations=n_cross_validations,
                    preprocess=True)

experiment = Experiment(ws, ExperimentName)
run = experiment.submit(config=automl_config, show_output=True)
    
best_model,fitted_model = run.get_output()

###############################################################################
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
    
###############################################################################
from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies

run_config = RunConfiguration(framework="python")
run_config.target = aml_compute
run_config.environment.docker.enabled = True
run_config.environment.docker.base_image = azureml.core.runconfig.DEFAULT_CPU_IMAGE

dependencies = CondaDependencies.create(
    pip_packages=["scikit-learn", "scipy", "numpy"])
run_config.environment.python.conda_dependencies = dependencies

from azureml.train.automl import AutoMLConfig
import time
import os
import logging

ExperimentName = "AutoML_Demo_Experiment_from_API"       
tasks = "classification"
iterations = 12
iteration_timeout_minutes = 6
primary_metric = "AUC_weighted"
aml_name = 'cpu-cluster'
from azureml.train.automl import AutoMLConfig
from azureml.core.experiment import Experiment        
#n_cross_validations = request.json['n_cross_validations']
automl_config = AutoMLConfig(
                    task=tasks,
                    X=x_df,
                    y=y_df,
                    compute_target=aml_name,
                    run_configuration=run_config,
                    iterations=iterations,
                    iteration_timeout_minutes=iteration_timeout_minutes,
                    primary_metric=primary_metric,
                    #n_cross_validations=n_cross_validations,
                    preprocess=True)

from azureml.core.experiment import Experiment
experiment = Experiment(ws, 'automl_remote')
remote_run = experiment.submit(automl_config, show_output=True)
best_model,fitted_model = remote_run.get_output()


delete = ws.delete(delete_dependent_resources=False, no_wait=False)























# create a TabularDataset from multiple paths in datastore
datastore_paths = [
                  (datastore, 'D:/Stock_Prediction/AutoML_Azure/stocks_data/stocks_data/2018Q4PredictionTestSet101.csv'),
                  (datastore, 'D:/Stock_Prediction/AutoML_Azure/stocks_data/stocks_data/2018Q4PredictionTestSet10.csv'),
                  (datastore, 'D:/Stock_Prediction/AutoML_Azure/stocks_data/stocks_data/2018Q4PredictionTrainedSet10.csv')
                 ]
stock_ds = Dataset.Tabular.from_delimited_files(path=datastore_paths)

# preview the first 3 rows of titanic_ds
stock_ds.take(3).to_pandas_dataframe()

stock_ds = stock_ds.register(workspace = ws,
                                 name = 'stock_ds',
                                 description = 'stock training data')


