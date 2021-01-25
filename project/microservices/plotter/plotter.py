import pandas as pd
import seaborn as sns 
import sys
import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA
import argparse


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()
parser.add_argument("--dataset_name", type=str, help="the name of the dataset to run on")
parser.add_argument("--user_name", type=str, help="the name of the user which the dataset belongs too", default="")

args = parser.parse_args()

print(args)
dataset_name = args.dataset_name

if args.user_name == "": 
    print("Hehe funny bunny")
else: 
    print(args.user_name)

sns.set_theme(style="ticks")
df = pd.read_csv(f"datasets/{dataset_name}.csv", header=None)

sns_plot = sns.pairplot(df, hue=len(df.columns)-1)
sns_plot.savefig(f"output/{dataset_name}_pair_plot.pdf")

f, ax = plt.subplots()
corr = df.corr()
hm = sns.heatmap(round(df.corr(),2), annot=True, cmap="coolwarm")
fig = hm.get_figure()
fig.savefig(f"output/{dataset_name}_heatmap.pdf")







if __name__=="__main__": 
    print(df)
    print(len(df.columns))