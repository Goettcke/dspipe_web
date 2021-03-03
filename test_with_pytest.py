#test_with_pytest.py
import pytest

#Tests if the testing system works, by running a test, that should always be true.
def test_uppercase():
    assert "loud noises".upper() == "LOUD NOISES"

def test_imports():
    import ds_pipe
    import flask
    import sqlalchemy
    import flask_login

def test_datasets():
    from ds_pipe.datasets.dataset_loader import Dataset_Collections
    dc = Dataset_Collections()
    dc_full_dict = dc.get_full_dictionary()
    print(len(dc_full_dict.keys()))
    assert len(dc_full_dict['iris'].target) == 150
    # Here we could be more thorough, and check that all the datasets were the correct length.


def test_algorithm():
    from ds_pipe.datasets.dataset_loader import Dataset_Collections
    from ds_pipe.evaluation.evaluation_methods import random_sampling_evaluator
    from ds_pipe.semi_supervised_classifiers.kNN_LDP import kNN_LDP
    dc = Dataset_Collections()
    dc_full_dict = dc.get_full_dictionary()
    algorithm = kNN_LDP(n_neighbors=10)
    results = random_sampling_evaluator(dc_full_dict['iris'], algorithm,
                                            percentage_labelled= 90,
                                            number_of_samples=10,
                                            quality_measure="accuracy")
    assert sum(results)/len(results) > 0.9

