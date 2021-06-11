# from azureml.core import Workspace
# ws = Workspace.create(name='handsonmlops',
#                       subscription_id='bf6a60a4-e47f-478a-9c72-537da82ba9b7',
#                       resource_group='lpu-1',
#                       create_resource_group=True,
#                       location='eastus2'
#                       )
# ws.write_config(path="./", file_name="ws_config.json")
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


# model = Model.register(
# workspace = ws, model_path = "churn-model.pkl", model_name = "churn-model-test")

model = Model(workspace=ws, name="churn-model-test")
# model.download(target_dir=os.getcwd())


###########################################################################


# Choose a name for your instance
# Compute instance name should be unique across the azure region
compute_name = "vms"

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


#####################################################################


# list_vms = AmlCompute.supported_vmsizes(workspace=ws)

compute_config = RunConfiguration()
compute_config.target = "vms"
compute_config.amlcompute.vm_size = "STANDARD_D1_V2"


dependencies = CondaDependencies()
dependencies.add_pip_package("sklearn")
dependencies.add_pip_package("numpy==1.15.4")
compute_config.environment.python.conda_dependencies = dependencies


script_run_config = ScriptRunConfig(source_directory=os.getcwd(
), script="train.py", run_config=compute_config)
experiment = Experiment(workspace=ws, name="traiming-experiment")
run = experiment.submit(config=script_run_config)
run.wait_for_completion(show_output=True)


##############################################################

# Register the model to deploy
#model = run.register_model(model_name = "chrun-model", model_path = "outputs/churn-model.pkl")

# Combine scoring script & environment in Inference configuration
inference_config = InferenceConfig(entry_script="model.py")

# Set deployment configuration
deployment_config = AciWebservice.deploy_configuration(cpu_cores=1,
                                                       memory_gb=1)
model = Model(workspace=ws, name="churn-model-test")
# Define the model, inference, & deployment configuration and web service name and location to deploy
service = Model.deploy(workspace=ws,
                       name="mywebservice",
                       models=[model],
                       inference_config=inference_config,
                       deployment_config=deployment_config)
