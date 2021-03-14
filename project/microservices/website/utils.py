import pandas as pd
from flask import flash
from app import supported_algorithms, supported_quality_measures, supported_datasets


def task_to_pandas_dataframe(task, id):
    task_dict = {
        "id": id, 
        "algorithm": task.algorithm,
        "number_of_samples": task.number_of_samples,
        "dataset": task.dataset_name,
        "n_neighbors": task.n_neighbors,
        "quality_measure":  task.quality_measure,
        "percent_labelled": task.percent_labelled,
        "alpha": task.alpha,
        "gamma": task.gamma,
        "evaluation_method": task.evaluation_method,
        "results": task.results
    }

    #return pd.DataFrame(task_dict)
    return task_dict


def get_result_parameters(file_):
    if file_.split(".")[-1] == "csv":
        #print("\n" + file_)
        file_split = file_.split("_")
        file_split = [split.replace(".csv","") for split in file_split]
        #print(file_split)
        file_dict = {split_.split("-")[0]: split_.split("-")[1] for split_ in file_split}
        #print(file_dict)
        return file_dict
    else:
        print("Please provide a .csv file")

def get_parameter_dict(parameter_string): 
        # Setting up the parameters.
        parameter_dict = {}
        parameters = parameter_string.split(" ")
        for parameter in parameters:
            k,v = parameter.split("=")
            parameter_dict[k] = v
        return parameter_dict

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

def check_parameters(algorithm, dataset_name, q_measure, number_of_samples, percent_labelled, parameters):
    parameters_check_out= True
    
    if algorithm not in supported_algorithms: 
        parameters_check_out = False
        flash(f"algorithm: {algorithm} is not supported pick, one from {supported_algorithms}")

    if dataset_name not in supported_datasets: 
        parameters_check_out = False
        flash(f"dataset: {dataset_name} is not supported pick, one from {supported_datasets}")

    if q_measure not in supported_quality_measures: 
        parameters_check_out = False
        flash(f"quality measure: {q_measure} is not supported, pick one from {supported_quality_measures}")

    if number_of_samples != "": 
        if int(number_of_samples) < 1 or int(number_of_samples) > 100: 
            parameters_check_out = False
            flash(f"number of samples: {number_of_samples} is not supported, pick a number between 1 and 100")
    else: 
        parameters_check_out = False
        flash(f"number of samples cannot be empty!")

    if percent_labelled != "": 
        if int(percent_labelled) < 1 or int(percent_labelled) > 99: 
            parameters_check_out = False
            flash(f"percent_labelled: {percent_labelled} is not supported, pick a number between 1 and 99")
    else: 
        parameters_check_out = False
        flash(f"percent_labelled cannot be empty!")
    
    if parameters != "": 
        parameter_value_dict = get_parameters(get_parameter_dict(parameters))
        keys = parameter_value_dict.keys()
        print(keys) 
        if algorithm=="knn_ldp" and "n_neighbors" not in keys:
            flash("You must have parameter k=something when testing the knn_ldp algorithm")
            parameters_check_out = False
        elif algorithm=="lp" and ('gamma' not in keys or 'n_neighbors' not in keys):
            flash("You must have parameter g=something or gamma=something when testing the lp algorithm, unless you use the knn kernel version of lp, then set k=somethin, unless you use the knn kernel version of lp, then set k=something")
            parameters_check_out = False

        elif algorithm=="ls" and (('gamma' not in keys and 'alpha' not in keys) or 'n_neighbors' not in keys):
            flash("You must have parameter g=something or gamma=something when testing the lp algorithm, unless you use the knn kernel version of lp, then set k=somethin, unless you use the knn kernel version of lp, then set k=something")
            parameters_check_out = False
        
   
    else: 
        parameters_check_out = False
        flash(f"Set some parameters for your test such as, n_neighbors=1 gamma=20 or alpha=0.2, abbr. (k, g, a)")
 

   

    return parameters_check_out
    
        



def split_df(df):
    import warnings
    from itertools import product

    # Find all types of quality measures
    print(df)
    q_measure_set = set(df['quality_measure'])
    print(q_measure_set)

    # Find all number_of samples
    number_of_samples_set = set(df['number_of_samples'])
    print(number_of_samples_set)

    evaluation_methods_set = set(df['evaluation_method'])
    print(evaluation_methods_set)

    (df['percent_labelled'])
    type(df['percent_labelled'])
    percent_labelled_set = set(df['percent_labelled'])
    print(percent_labelled_set)

    assert len(q_measure_set) > 0
    assert len(number_of_samples_set) > 0
    assert len(evaluation_methods_set) > 0
    assert len(percent_labelled_set) > 0
    sub_dfs = []
    warnings.simplefilter(action="ignore", category=UserWarning)
    for quality_measure, number_of_samples, evaluation_method, percent_labelled in product(q_measure_set, number_of_samples_set, evaluation_methods_set, percent_labelled_set):
        #print(quality_measure)
        sub_df = df[df.quality_measure == quality_measure][df.number_of_samples == number_of_samples][df.percent_labelled == percent_labelled][df.evaluation_method == evaluation_method]
        if len(sub_df) > 0:
            print(sub_df)
            sub_dfs.append(sub_df)
    return sub_dfs


def get_html_tables(df):
    data_frames = split_df(df)
    tables = []
    for df_ in data_frames:
    #    table_head = f"<div class='row'>  <table class = 'table table-striped table-dark'>\n  <thead> \n   <tr>\n <th scope='col'>algorithm</th> <th scope='col'>Number of samples</th> <th scope='col'>Dataset</th><th scope='col'>n_neighbors</th> <th scope='col'>Quality measure</th> <th scope='col'>Percent labelled</th> <th scope='col'>alpha</th><th scope='col'>gamma</th><th scope='col'>Results</th>  </tr></thead></div> \n"
        table_content = df_.to_html(classes = "table table-striped", header=True)
        #return div_top + heading + "<div class='row'>\n" + table + "</div>\n</div> <hr/>\n"
        tables.append(table_content)
    return tables



