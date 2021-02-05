import argparse
import os
from ds_pipe.datasets.dataset_loader import Dataset_Collections
from ds_pipe.evaluation.evaluation_methods import random_sampling_evaluator
from ds_pipe.semi_supervised_classifiers.kNN_LDP import kNN_LDP
from sklearn.semi_supervised import LabelSpreading, LabelPropagation

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
parser.add_argument("--dataset_name", type=str, help="the name of the dataset to run on")
parser.add_argument("--user_id", type=int, help="the name of the user which the dataset belongs too", default=0)
parser.add_argument("--percent_labelled", type=int, help="How many percent labelled data the user wants to use for the test", default=10)
parser.add_argument("--algorithm", type=str, help="The Algorithm to use for the test", default="knn_ldp")
parser.add_argument("--number_of_samples", type=int, help="The number of samples to use in the test", default=10)
parser.add_argument("--quality_measure", type=str, help="The quality measure to use in the test. Currently accuracy and f1 is supported.", default="accuracy")
parser.add_argument("--n_neighbors", type=int, help="If algorithm takes an n_neighbors argument", default=10)
parser.add_argument("--gamma", type=float, help="The gamma value to use for methods using an RBF kernel", default=20) # Same defaults used as in Scikit-learn
parser.add_argument("--alpha", type=float, help="The alpha value to use for Label Spreading (learning with Local and Global Consistency", default=0.2)
parser.add_argument("--kernel", type=str, help="For LP and LS, they kan work with different kernels, chose either rbf og knn", default="rbf")
args = parser.parse_args()

# TODO for the algorithm parameter provide options

"""
The most basic runner, which starts chewing through the database until it is empty - using knn_ldp
TODO 1. Allow different quality measures
TODO 2. Allow different classifiers
TODO 3. Different configurations of classifiers (parameters)
:return: None
"""
dc = Dataset_Collections()
dc_full_dict = dc.get_full_dictionary()

# Check if the user folder is created:
user_folder = f"/app/output/results/{args.user_id}" 

if not os.path.exists(user_folder): 
    os.makedirs(user_folder)


if args.algorithm == "knn_ldp": 
    algorithm = kNN_LDP(n_neighbors = args.n_neighbors)
    f = open(f"{user_folder}/pl-{args.percent_labelled}_ns-{args.number_of_samples}_q-{args.quality_measure}_n-{args.n_neighbors}.csv", "a+")

elif args.algorithm == "lp": 
    if args.kernel == "rbf":
        algorithm = LabelPropagation(gamma=args.gamma)
        f = open(f"{user_folder}/pl-{args.percent_labelled}_ns-{args.number_of_samples}_q-{args.quality_measure}_g-{args.gamma}.csv", "a+")
    else: 
        algorithm = LabelPropagation(n_neighbors=args.n_neighbors)
        f = open(f"{user_folder}/pl-{args.percent_labelled}_ns-{args.number_of_samples}_q-{args.quality_measure}_n-{args.n_neighbors}.csv", "a+")

elif args.algorithm == "ls": 
    if args.kernel == "rbf":
        algorithm = LabelSpreading(gamma=args.gamma, alpha=args.alpha)
        f = open(f"{user_folder}/pl-{args.percent_labelled}_ns-{args.number_of_samples}_q-{args.quality_measure}_g-{args.gamma}_a-{args.alpha}.csv", "a+")
    else: 
        algorithm = LabelSpreading(n_neighbors=args.n_neighbors)
        f = open(f"{user_folder}/pl-{args.percent_labelled}_ns-{args.number_of_samples}_q-{args.quality_measure}_n-{args.n_neighbors}.csv", "a+")
else: 
    raise Exception("Unsupported algorithm - knn_ldp, lp and ls is currently the only supported algorithms")


results = random_sampling_evaluator(dc_full_dict[args.dataset_name], algorithm,
                                    percentage_labelled=args.percent_labelled,
                                    number_of_samples=args.number_of_samples,
                                    quality_measure=args.quality_measure)

result_string = ", ".join([str(result) for result in results])
f.write(f"{args.algorithm}, {args.dataset_name}, {result_string}\n")
f.close()
