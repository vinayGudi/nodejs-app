from azureml.core.webservice import AciWebservice, Webservice
from azureml.core.model import InferenceConfig, Model
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.compute_target import ComputeTargetException
from azureml.core.compute import ComputeTarget, ComputeInstance
import time
import datetime
from azureml.core import ScriptRunConfig
from azureml.core.compute import AmlCompute
from azureml.core.runconfig import RunConfiguration
import os
from azureml.core.model import Model
from azureml.core.experiment import Experiment
from azureml.core import Workspace
ws = Workspace.get(name="demo-mltraining",
                   subscription_id='efd07289-8385-4080-98f7-5654eae372b9', resource_group='loopr-dev')


compute_name = "vmss"
instance = ComputeInstance(workspace=ws, name=compute_name)
instance.delete(wait_for_completion=True, show_output=True)
