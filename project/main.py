import os
from time import sleep
from flask import render_template, url_for, request, redirect, Blueprint
from flask_login import current_user, login_required
import pandas as pd 
from datetime import datetime


from ds_pipe.datasets.dataset_loader import Dataset_Collections
from ds_pipe.evaluation.evaluation_methods import random_sampling_evaluator
from ds_pipe.semi_supervised_classifiers.kNN_LDP import kNN_LDP
from project.models import Todo
from project import db

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
        task.dataset_name = request.form['dataset_name']
        task.per_un = request.form['percent_unlabelled']
        task.number_of_samples = request.form['number_of_samples']
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
        dc = Dataset_Collections()
        dc_full_dict = dc.get_full_dictionary()

        # Check if the user folder is created:
        user_folder = f"output/results/{current_user.id}" 
        if not os.path.exists(user_folder): 
            os.makedirs(user_folder)

        for task in tasks:
            if task.dataset_name in dc_full_dict.keys():
                algorithm = kNN_LDP(n_neighbors=10)
                results = random_sampling_evaluator(dc_full_dict[task.dataset_name], algorithm,
                                                    percentage_labelled=100 - task.per_un,
                                                    number_of_samples=task.number_of_samples,
                                                    quality_measure="accuracy")
                print(results)
                f = open(f"{user_folder}/{task.per_un}_{task.number_of_samples}.csv", "a+")
                result_string = ", ".join([str(result) for result in results])
                f.write(f"{task.dataset_name}, {result_string}\n")
                f.close()
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
    # TODO find the jobs that are particular for that the current user name. 
    # TODO Add a navbar to this page containing Schedule, Results, Logout 
    
    if request.method == 'POST':
        dataset_name = request.form['dataset_name']
        percent_unlabelled = request.form['percent_unlabelled']
        number_of_samples = request.form['number_of_samples']
        new_task = Todo(dataset_name=dataset_name, per_un=percent_unlabelled, number_of_samples=number_of_samples, user_id=current_user.id)
        try:
            db.session.add(new_task)
            db.session.commit()
            #render_template('example_profile_page.html', name=current_user.name) 
            return redirect(url_for('main.profile'))
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.filter(Todo.user_id == current_user.id).order_by(Todo.date_created).all()
        dc = Dataset_Collections()
        datasets = dc.keel_datasets() + dc.chapelle_datasets()
        dataset_meta_information = [(dataset_name,  len(dataset.data[0]), len(dataset.target)) for dataset, dataset_name in datasets]
        return render_template('profile.html', name=current_user.name, tasks=tasks, dataset_meta=dataset_meta_information)


@main.route('/results', methods=['GET'])
@login_required
def results():
    user_folder = f"output/results/{current_user.id}/"
    result_files = os.listdir(user_folder)
    user_results = [pd.read_csv(user_folder + result_file) for result_file in result_files]

    tables = [result.to_html(classes = "table table-striped", header=True, escape=False) for result in user_results] 
    for table in tables: 
        print(table)
    return render_template('results.html', tables=tables)

@main.route("/deploy")
def deploy(): 
    os.system("~/myproject/./deploy.sh")
    return render_template("deploy.html")