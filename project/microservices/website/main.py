import os
import sys
from time import sleep
from flask import render_template, url_for, request, redirect, Blueprint, send_file
from flask_login import current_user, login_required
from datetime import datetime

# Setting up the GRPC
import grpc
from ds_pipe_task_pb2_grpc import RunnerStub, Task_EvaluatorStub
from ds_pipe_task_pb2 import Task # Uff this is basically the same name as task

#from ds_pipe.datasets.dataset_loader import Dataset_Collections
from ds_pipe.evaluation.evaluation_methods import random_sampling_evaluator
from ds_pipe.semi_supervised_classifiers.kNN_LDP import kNN_LDP
from models import Todo
from app import db, dc_full_dict, dc, datasets, dataset_meta_information
from utils import get_html_table

main = Blueprint('main', __name__)

evaluators_host = os.getenv("EVALUATORS_HOST", "localhost")
evaluators_channel = grpc.insecure_channel(f"{evaluators_host}:50050")
evaluators_client = Task_EvaluatorStub(evaluators_channel)


@main.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('main.profile'))

    except:
        return 'There was a problem deleting that task'


@main.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.algorithm = request.form['algorithm']
        task.q_measure = request.form['q_measure']
        task.dataset_name = request.form['dataset_name']
        task.per = request.form['percent_labelled']
        task.number_of_samples = request.form['number_of_samples']
        task.parameters = request.form['parameters']

        #TODO check if this format can run before submitting it. Return an error page with instructions on what you can run.

        try:
            db.session.commit()
            return redirect(url_for('main.profile'))
        except Exception as e:
            print(e)
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)

def get_parameters(parameter_dict):
    parameter_value_dict = {}
    if "k" in parameter_dict.keys():
        parameter_value_dict["n_neighbors"] = int(parameter_dict["k"])

    elif "n_neighbors" in parameter_dict.keys():
        parameter_value_dict["n_neighbors"] = int(parameter_dict["n_neighbors"])
    else:
        parameter_value_dict["n_neighbors"] = 10

    if "g" in parameter_dict.keys():
        parameter_value_dict["gamma"] = float(parameter_dict["g"])

    elif "gamma" in parameter_dict.keys():
        parameter_value_dict["gamma"] = float(parameter_dict["gamma"])
    else:
        parameter_value_dict["gamma"] = 20

    if "a" in parameter_dict.keys():
        parameter_value_dict["alpha"] = float(parameter_dict["a"])

    elif "alpha" in parameter_dict.keys():
        parameter_value_dict["alpha"] = float(parameter_dict["alpha"])
    else:
        parameter_value_dict["alpha"] = 0.2

    return parameter_value_dict



@main.route('/run', methods=['POST'])
def run():
    """
    The most basic runner, which starts chewing through the database until it is empty - using knn_ldp
    TODO 1. Allow different quality measures
    TODO 2. Allow different classifiers
    TODO 3. Different configurations of classifiers (parameters)
    :return: None
    """

    if request.method == 'POST':
        error_log = "output/log.txt"
        tasks = Todo.query.filter(Todo.user_id == current_user.id).order_by(Todo.date_created).all()

        for task in tasks:
            if task.dataset_name in dc_full_dict.keys():

                # Setting up the parameters.
                parameter_dict = {}
                parameters = task.parameters.split(" ")
                for parameter in parameters:
                    k,v = parameter.split("=")
                    parameter_dict[k] = v


                if task.algorithm == "ls":
                    if "k" in parameter_dict.keys():
                        algorithm = "ls_knn"
                    else:
                        algorithm = "ls_rbf"

                if task.algorithm == "lp":
                    if "k" in parameter_dict.keys():
                        algorithm = "lp_knn"
                    else:
                        algorithm = "lp_rbf"
                else:
                    algorithm = "knn_ldp"

                parameter_value_dict = get_parameters(parameter_dict)

                task_request = Task(
                    user_id = current_user.id,
                    algorithm = algorithm,
                    number_of_samples = task.number_of_samples,
                    dataset_name = task.dataset_name,
                    n_neighbors = parameter_value_dict['n_neighbors'],
                    quality_measure = task.q_measure,
                    percent_labelled = task.per,
                    alpha = parameter_value_dict['alpha'],
                    gamma = parameter_value_dict['gamma'],
                    evaluation_method = "random_sampling"
                )

                evaluators_response = evaluators_client.Evaluate_Task(task_request)
                print(type(evaluators_response))

            else:
                f = open(error_log, "a+")
                f.write(f"{task.dataset_name} not in datasets,{datetime.utcnow()}\n")
                f.close()

        delete(task.id)
        print("No more jobs in queue")
        return redirect(url_for('main.profile'))

    else:
        return "There was an error with the backend - cannot run the tasks"


@main.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    if request.method == 'POST':
        algorithm = request.form['algorithm']
        dataset_name = request.form['dataset_name']
        q_measure = request.form['q_measure']
        percent_labelled = request.form['percent_labelled']
        number_of_samples = request.form['number_of_samples']
        parameters = request.form['parameters']

        # Check add the form check here! Or add javascript to check the form before it is submitted

        new_task = Todo(algorithm = algorithm,
                        q_measure = q_measure,
                        dataset_name=dataset_name,
                        per=percent_labelled,
                        number_of_samples=number_of_samples,
                        user_id=current_user.id,
                        parameters=parameters)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('main.profile'))

        except Exception as e:
            print(e)
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.filter(Todo.user_id == current_user.id).order_by(Todo.date_created).all()
        datasets = dc.keel_datasets() + dc.chapelle_datasets()
        dataset_meta_information = [(dataset_name,  len(dataset.data[0]), len(dataset.target)) for dataset, dataset_name in datasets]
        return render_template('profile.html', name=current_user.name, tasks=tasks, dataset_meta=dataset_meta_information, user_type=current_user.user_type)


@main.route('/results', methods=['GET'])
@login_required
def results():
    # TODO make a model locally, that we can interact with!
    tables = []
    all_parameters = []

    for result_file in result_files:
        tables.append(get_html_table(user_folder + result_file))

    return render_template('results.html', tables=tables)

@main.route('/admin_panel')
@login_required
def admin_panel():
    if current_user.user_type == "base":
        return "<h1>You shall not pass!</h1>"
    else:
        return render_template('admin.html')

@main.route("/greet")
@login_required
def greet():
    return render_template("example_profile_page.html", name=current_user.name)

