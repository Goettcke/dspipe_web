import pandas as pd

def task_to_pandas_dataframe(task):
    task_dict = {
        "algorithm": task.algorithm,
        "number_of_samples": task.number_of_samples,
        "dataset": task.dataset_name,
        "n_neighbors": task.n_neighbors,
        "quality_measure":  task.quality_measure,
        "percent_labelled": task.percent_labelled,
        "alpha": task.alpha,
        "gamma": task.gamma,
        "evaluation_method": task.evaluation_method
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

        div_top = "<div class = 'container'>\n"

        table_head = f"<div class='row'>  <table class = 'table table-striped table-dark'>\n  <thead> \n   <tr>\n <th scope='col'>algorithm</th> <th scope='col'>Number of samples</th>  <th scope='col'>Quality measure</th> <th scope='col'>Percent labelled</th> <th scope='col'></th>  </tr></thead></div> \n"



        """
        table_content = f"<tbody>
                          <th scope='row'>{parameters['alg']}</th>
                             <td>{parameters['ns']}</td>
                             <td>{parameters['q']}</td>
                             <td>{parameters['pl']}</td>
                             <td>{parameters['n']}</td>
                          </tbody></table>
                        </div> \n"
        heading = table_head + table_content


        """
        #df.columns = ["algorithm", "dataset"] + [str(x) for x in list(range(df.shape[0]-2))]
        df_ = df.multiply(100)
        df_ = df.round(2)

        table = df_.to_html(classes = "table table-striped", header=True)
        #return div_top + heading + "<div class='row'>\n" + table + "</div>\n</div> <hr/>\n"
        div_bottom = "</div>\n</div> <hr/>\n"
        table = div_top + table_head +  "<div class='row'>\n" + table + div_bottom

        tables.append(table)

    return tables



