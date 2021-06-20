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
