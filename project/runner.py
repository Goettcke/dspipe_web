"""
File intended too loop through the database of tasks, and run the work in the queue.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from main import Todo, delete
from ds_pipe.datasets.dataset_loader import Dataset_Collections
from ds_pipe.evaluation.evaluation_methods import random_sampling_evaluator
from ds_pipe.semi_supervised_classifiers.kNN_LDP import kNN_LDP
from datetime import datetime

# TODO 2: Verify that the job makes sense, and add it to the run queue.
#  The rabbit MQ stream with microservices can be defined at a later point.
# TODO 3: Log the result of the run after the run is over in a database system, that handles concurrent inserts.

error_log = "output/log.txt"


def base_runner():
    """
    The most basic runner, which starts chewing through the database until it is empty.
    TODO 1. Allow different quality measures
    TODO 2. Allow different classifiers
    :return: None
    """
    tasks = Todo.query.order_by(Todo.date_created).all()
    # Task extracted - now it's time for running the stuff!
    dc = Dataset_Collections()
    dc_full_dict = dc.get_full_dictionary()
    for task in tasks:
        if task.dataset_name in dc_full_dict.keys():
            algorithm = kNN_LDP(n_neighbors=10)
            results = random_sampling_evaluator(dc_full_dict[task.dataset_name], algorithm, percentage_labelled=100-task.per_un,
                                      number_of_samples=task.number_of_samples, quality_measure="accuracy")
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



if __name__ == "__main__":
    base_runner()
