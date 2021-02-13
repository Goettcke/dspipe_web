import os
import pika, sys, json
from time import sleep
from flask import render_template, url_for, request, redirect, Blueprint, send_file
from flask_login import current_user, login_required
import pandas as pd
from datetime import datetime


#from ds_pipe.datasets.dataset_loader import Dataset_Collections
from ds_pipe.evaluation.evaluation_methods import random_sampling_evaluator
from ds_pipe.semi_supervised_classifiers.kNN_LDP import kNN_LDP
from project.models import Todo
from project import db, dc_full_dict, dc, datasets, dataset_meta_information
from project.utils import get_html_table

main = Blueprint('main', __name__)



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
        # Task extracted - now it's time for running the stuff!
        # dc = Dataset_Collections() # This should really be removed for a snappier website
        # dc_full_dict = dc.get_full_dictionary()

        for task in tasks:
            if task.dataset_name in dc_full_dict.keys():
                connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

                channel = connection.channel()
                channel.queue_declare(queue="task_queue", durable=True)

                parameter_dict = {}
                parameters = task.parameters.split(" ")
                for parameter in parameters:
                    k,v = parameter.split("=")
                    parameter_dict[k] = v

                if "kernel" in parameter_dict.keys():
                    kernel = parameter_dict["kernel"]
                else:
                    kernel = "rbf"

                if "k" in parameter_dict.keys():
                    n_neighbors = parameter_dict["k"]
                else:
                    n_neighbors = 10

                if "a" in parameter_dict.keys():
                    alpha = parameter_dict["a"]
                else:
                    alpha = 0.2

                if "g" in parameter_dict.keys():
                    gamma = parameter_dict["g"]
                else:
                    gamma = 20

                message = json.dumps({"user_id": current_user.id,
                                      "algorithm": task.algorithm,
                                      "number_of_samples": task.number_of_samples,
                                      "dataset_name": task.dataset_name,
                                      "n_neighbors":n_neighbors,
                                      "quality_measure": task.q_measure,
                                      "percent_labelled":task.per,
                                      "alpha":alpha,
                                      "gamma":gamma,
                                      "kernel":kernel})

                channel.basic_publish(exchange="",
                                    routing_key="task_queue",
                                    body=message,
                                    properties=pika.BasicProperties(
                                    delivery_mode = 2,
                                    ))
                print(" [x] Sent %r " % message)
                connection.close()

            else:
                f = open(error_log, "a+")
                f.write(f"{task.dataset_name} not in datasets,{datetime.utcnow()}\n")
                f.close()
            delete(task.id)
        print("No more jobs in queue")
        return redirect(url_for('main.profile'))

    else:
        return "There was an with the backend - cannot run the tasks"

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
    user_folder = f"../../../runner_results/ds_pipe_runner/output/results/{current_user.id}/"
    result_files = os.listdir(user_folder)
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

