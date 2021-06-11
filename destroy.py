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
ws = Workspace.get(name="handsonmlops",
                   subscription_id='bf6a60a4-e47f-478a-9c72-537da82ba9b7', resource_group='lpu-1')


compute_name = "vmss"
instance = ComputeInstance(workspace=ws, name=compute_name)
instance.delete(wait_for_completion=True, show_output=True)
