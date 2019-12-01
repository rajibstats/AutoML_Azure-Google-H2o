# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 17:20:22 2019

@author: datacore
"""

from azureml.core.authentication import AzureCliAuthentication
import azure.cli.core
#cli_auth = AzureCliAuthentication()
from azureml.core.workspace import Workspace

ws = Workspace(subscription_id="24075937-2687-4457-bac6-ec16dec514c3",
               resource_group="VstsRG-784AbhijitC-8a31",
               workspace_name="automldc")

from azureml.core.experiment import Experiment
from azureml.core import Run
experiment=Experiment(ws, 'Myexp2_v1_test21')
best_run = Run(experiment=experiment, run_id='AutoML_74e9d9dc-f347-4392-b8bb-3edeb4a6afad_8')
fitted_model = Run(experiment=experiment, run_id='AutoML_74e9d9dc-f347-4392-b8bb-3edeb4a6afad_8')
#print(best_run.register_model()
print(fitted_model)



# Get a dataset by name
from azureml.core.dataset import Dataset

file_name = '2018Q4PredictionTrainedSet101.csv'
stock_dataset = Dataset.get_by_name(ws, '2018Q4PredictionTrainedSet101.csv')
#stock_dataset
#dataset = Dataset.Tabular.from_delimited_files(stock_dataset)
stock_dataset.to_pandas_dataframe().describe()
stock_dataset.take(3).to_pandas_dataframe()

X = stock_dataset.drop_columns(columns=[ 'ActionTaken'])
y = stock_dataset.keep_columns(columns=['ActionTaken'], validate=True)
print(y)
#print('X and y are ready!')
stock_dataset_df = stock_dataset.to_pandas_dataframe()
y_df = stock_dataset_df['ActionTaken'].values
x_df = stock_dataset_df.drop(['ActionTaken'], axis=1)

y_predict = fitted_model.predict(x_df)
print(y_predict)