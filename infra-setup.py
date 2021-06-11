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

experiment = Experiment(workspace=ws, name='training-experiment')
list_experiments = Experiment.list(ws)
print(list_experiments)


compute_name = "vmss"

# Verify that instance does not exist already
try:
    instance = ComputeInstance(workspace=ws, name=compute_name)
    print('Found existing instance, use it.')
    list_vms = AmlCompute.supported_vmsizes(workspace=ws)
    compute_config = RunConfiguration()
    compute_config.target = "amlcompute"
    compute_config.amlcompute.vm_size = "STANDARD_D1_V2"
except ComputeTargetException:
    compute_config = ComputeInstance.provisioning_configuration(
        vm_size='STANDARD_D3_V2',
        ssh_public_access=False,
        # vnet_resourcegroup_name='<my-resource-group>',
        # vnet_name='<my-vnet-name>',
        # subnet_name='default',
        # admin_user_ssh_public_key='<my-sshkey>'
    )
    instance = ComputeInstance.create(ws, compute_name, compute_config)
    instance.wait_for_completion(show_output=True)
