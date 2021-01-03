import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from ds_pipe.datasets.dataset_loader import Dataset_Collections
from ds_pipe.evaluation.evaluation_methods import random_sampling_evaluator
from ds_pipe.semi_supervised_classifiers.kNN_LDP import kNN_LDP



db_name = "test.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+db_name
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dataset_name = db.Column(db.String(200), nullable=False)
    per_un = db.Column(db.Integer, nullable=False)
    number_of_samples = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Task {self.dataset_name}>"


if not os.path.exists(db_name):
    print("\n* ds_pipe web notification : Automatically created the test.db file\n")
    db.create_all()  # Creating the database, if it doesn't exist.


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        dataset_name = request.form['dataset_name']
        percent_unlabelled = request.form['percent_unlabelled']
        number_of_samples = request.form['number_of_samples']
        new_task = Todo(dataset_name=dataset_name, per_un=percent_unlabelled, number_of_samples=number_of_samples)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        dc = Dataset_Collections()
        datasets = dc.keel_datasets() + dc.chapelle_datasets()
        dataset_meta_information = [(dataset_name,  len(dataset.data[0]), len(dataset.target)) for dataset, dataset_name in datasets]
        return render_template('index.html', tasks=tasks, dataset_meta=dataset_meta_information)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.dataset_name = request.form['dataset_name']
        task.per_un = request.form['percent_unlabelled']
        task.number_of_samples = request.form['number_of_samples']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


@app.route('/run/', methods=['POST'])
def run():
    """
    The most basic runner, which starts chewing through the database until it is empty.
    TODO 1. Allow different quality measures
    TODO 2. Allow different classifiers
    :return: None
    """
    if request.method == 'POST':
        error_log = "output/log.txt"
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Task extracted - now it's time for running the stuff!
        dc = Dataset_Collections()
        dc_full_dict = dc.get_full_dictionary()
        for task in tasks:
            if task.dataset_name in dc_full_dict.keys():
                algorithm = kNN_LDP(n_neighbors=10)
                results = random_sampling_evaluator(dc_full_dict[task.dataset_name], algorithm,
                                                    percentage_labelled=100 - task.per_un,
                                                    number_of_samples=task.number_of_samples,
                                                    quality_measure="accuracy")
                print(results)
                f = open(f"output/results_{task.per_un}_{task.number_of_samples}.csv", "a+")
                result_string = ", ".join([str(result) for result in results])
                f.write(f"{task.dataset_name}, {result_string}\n")
                f.close()
            else:
                f = open(error_log, "a+")
                f.write(f"{task.dataset_name} not in datasets,{datetime.utcnow()}\n")
                f.close()
            delete(task.id)
        print("No more jobs in queue")
        return redirect('/')

    else:
        return "There was an with the backend - cannot run the tasks"



if __name__ == "__main__":
    app.run(debug=True)
