# marketplace/marketplace.py
import os
from flask import Flask, render_template
import grpc

from ds_pipe_task_pb2 import Task
from ds_pipe_task_pb2_grpc import RunnerStub, Task_EvaluatorStub

app = Flask(__name__)

"""
runners_host = os.getenv("RUNNERS_HOST", "localhost")
runners_channel = grpc.insecure_channel(f"{runners_host}:50051")
runners_client = RunnerStub(runners_channel)
"""

evaluators_host = os.getenv("EVALUATORS_HOST", "localhost")
evaluators_channel = grpc.insecure_channel(f"{evaluators_host}:50050")
evaluators_client = Task_EvaluatorStub(evaluators_channel)


@app.route("/")
def render_homepage():
    task_request = Task(
        user_id = 1,
        algorithm = "ls_rbf",
        number_of_samples = 10,
        dataset_name = "iris",
        n_neighbors = 10,
        quality_measure = "accuracy",
        percent_labelled = 50,
        alpha = 0.2,
        gamma = 20,
        kernel = "blarg", # is obsolete - kernel modifications are considered different algorithm
        evaluation_method = "random_sampling"
    )
    #runners_response = runners_client.Run_task(task_request)
    evaluators_response = evaluators_client.Evaluate_Task(task_request)

    return render_template(
        "homepage.html",
        #results=runners_response.results, dataset=task_request.dataset_name
        results=evaluators_response.results, dataset=task_request.dataset_name
    )
