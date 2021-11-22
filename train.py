# TODO: PULL AND START DOCKER CONTAINER

from clearml import Task, StorageManager

# Get game build and config file
remote_path="s3://experiment-logging/pretrained/longformer-base-4096" #TODO: replace path
local_path="~/results"
StorageManager.download_folder(remote_path, local_path, match_wildcard=None, overwrite=True)
print(f'\n Downloaded data to {local_path}\n')

# Create task
task = Task.init(project_name="mlagents", task_name="basedef", output_uri="s3://experiment-logging/storage/") #output folder from clearml
task.execute_remotely(queue_name="128RAMv100", exit_process=True)

import subprocess

# Run training
subprocess.run("mlagents-learn ~/agents.yaml --run-id testaip --env ~/linuxbuild/ss3build.x86_64 --results-dir ~/results")

# upload training results to bucket
local_path="~/results"
remote_path="s3://experiment-logging/pretrained/longformer-base-4096" #TODO: replace path
StorageManager.upload_folder(local_path, remote_path, match_wildcard=None)
print(f'\n Uploaded data to {remote_path}\n')

task.upload_artifact('model', artifact_object=os.path.join("models", "muc4", "model.tar.gz")) #TODO: weights are part of results folder. do i need this?
task.upload_artifact('train_metrics', artifact_object=os.path.join('models', 'muc4', "metrics.json"))

task.close()