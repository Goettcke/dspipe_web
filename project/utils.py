import pandas as pd
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

def get_html_table(df):


"""
    div_top = "<div class = 'container'>\n"
    if algorithm == "knnldp":
        table_head = "<div class='row'> <table class = 'table table-striped table-dark'>\n <thead> \n  <tr>\n     <th scope='col'>algorithm</th> <th scope='col'>Number of Samples</th> <th scope='col'>Quality measure</th> <th scope='col'>Percent labelled</th> <th scope='col'>n neighbors</th> </tr></thead>"

        table_content = f"<tbody> <th scope='row'>{parameters['alg']}</th> <td>{parameters['ns']}</td> <td>{parameters['q']}</td><td>{parameters['pl']}</td> <td>{parameters['n']}</td> </tbody></table> </div> \n"
        heading = table_head + table_content

    elif algorithm == "ls" :
        if 'g' in parameters.keys(): # Here we are checking which kernel was used in the configuration of the classifier
            table_head = "<div class='row'> <table class = 'table table-striped table-dark'>\n <thead> \n  <tr>\n     <th scope='col'>algorithm</th> <th scope='col'>Number of Samples</th> <th scope='col'>Quality measure</th> <th scope='col'>Percent labelled</th> <th scope='col'>gamma</th> <th scope='col'>alpha</th> </tr></thead>"
            table_content = f"<tbody> <th scope='row'>{parameters['alg']}</th> <td>{parameters['ns']}</td> <td>{parameters['q']}</td><td>{parameters['pl']}</td> <td>{parameters['g']} </td> <td>{parameters['a']} </td> </tbody></table> </div> \n"
        elif 'n' in parameters.keys():
            table_head = "<div class='row'> <table class = 'table table-striped table-dark'>\n <thead> \n  <tr>\n     <th scope='col'>algorithm</th> <th scope='col'>Number of Samples</th> <th scope='col'>Quality measure</th> <th scope='col'>Percent labelled</th> <th scope='col'>n neighbors</th> </tr></thead>"
            table_content = f"<tbody> <th scope='row'>{parameters['alg']}</th> <td>{parameters['ns']}</td> <td>{parameters['q']}</td><td>{parameters['pl']}</td> <td>{parameters['n']} </td> </tbody></table> </div> \n"
        heading = table_head + table_content

    elif algorithm == "lp":
        if 'g' in parameters.keys(): # Here we are checking which kernel was used in the configuration of the classifier
            table_head = "<div class='row'> <table class = 'table table-striped table-dark'>\n <thead> \n  <tr>\n     <th scope='col'>algorithm</th> <th scope='col'>Number of Samples</th> <th scope='col'>Quality measure</th> <th scope='col'>Percent labelled</th> <th scope='col'>gamma</th> </tr></thead>"
            table_content = f"<tbody> <th scope='row'>{parameters['alg']}</th> <td>{parameters['ns']}</td> <td>{parameters['q']}</td><td>{parameters['pl']}</td> <td>{parameters['g']} </td>  </tbody></table> </div> \n"
        elif 'n' in parameters.keys():
            table_head = "<div class='row'> <table class = 'table table-striped table-dark'>\n <thead> \n  <tr>\n     <th scope='col'>algorithm</th> <th scope='col'>Number of Samples</th> <th scope='col'>Quality measure</th> <th scope='col'>Percent labelled</th> <th scope='col'>n neighbors</th> </tr></thead>"
            table_content = f"<tbody> <th scope='row'>{parameters['alg']}</th> <td>{parameters['ns']}</td> <td>{parameters['q']}</td><td>{parameters['pl']}</td> <td>{parameters['n']} </td>  </tbody></table> </div> \n"

        heading = table_head + table_content
"""
    df = pd.read_csv(result_file_path, header=None, names = list(range(int(parameters['ns']))))
    #df.columns = ["algorithm", "dataset"] + [str(x) for x in list(range(df.shape[0]-2))]
    df = df.multiply(100)
    df = df.round(2)
    table = df.to_html(classes = "table table-striped", header=True)
    return div_top + heading + "<div class='row'>\n" + table + "</div>\n</div> <hr/>\n"
