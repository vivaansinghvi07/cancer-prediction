import csv                          # view data
import matplotlib.pyplot as plt     # plotting resutls
import numpy as np
import pandas as pd

# columns to use as reference when doing the analysis: 
# these are possible symtoms one might face if they have lung cancer
SYMPTOMS = ["YELLOW_FINGERS", "COUGHING", "SHORTNESS OF BREATH", "SWALLOWING DIFFICULTY", "CHEST PAIN", "WHEEZING", "FATIGUE", "YELLOW_FINGERS"]
# these are factors which may or may not lead to lung cancer
CAUSES = ["SMOKING", "ALCOHOL CONSUMING", "ANXIETY"]

# for cleaning up data and adding newlines when text is too long
def add_newlines(str):
    return str.replace(" ", "\n", 1)

def plot(method):

    # label for graph, depending on what is being analyzed
    x_label = ["Causes", "Symptoms"][int(method) - 1]

    # obtain measurements
    df = pd.read_csv("lung-cancer/data/lung-cancer.csv", usecols=eval(x_label.upper()))
    cancer_results = pd.read_csv("lung-cancer/data/lung-cancer.csv", usecols=["LUNG_CANCER"])["LUNG_CANCER"]

    # determines bar heights
    yes_symptom_yes_cancer = []
    no_symptom_yes_cancer = []
    for stat in df:

        # stores counts of people
        total_count = yes_count = no_count = 0

        # stores results and goes through each one
        results = df[stat]
        for person in range(len(results)):
        
            # checks if they said no to having cancer
            if cancer_results[person] == "NO":    
                continue

            # appends counts accordingly
            if results[person] == 2:
                yes_count += 1
            else:
                no_count += 1
            total_count += 1

        # determines percents
        yes_symptom_yes_cancer.append(yes_count / total_count * 100)
        no_symptom_yes_cancer.append(no_count / total_count * 100)

    # creates arrays of 100 percents
    yes_symptom_no_cancer = [100 for _ in range(len(yes_symptom_yes_cancer))]
    no_symptom_no_cancer = [100 for _ in range(len(no_symptom_yes_cancer))]

    # settings for plot
    stat_count = len(yes_symptom_yes_cancer)
    x_size, y_size = 10, 6
    fig = plt.figure(figsize=(x_size, y_size))
    bar_width = x_size / stat_count / 3

    # determines x-axis
    x_axis = np.arange(0, x_size, x_size / stat_count)

    # plots yes_cancer bar
    plt.bar(x_axis, yes_symptom_no_cancer, bar_width, color="lightblue", label="Symptom, No Cancer")
    plt.bar(x_axis, yes_symptom_yes_cancer, bar_width, color="royalblue", label="Symptom, Cancer")

    plt.bar(x_axis + bar_width * 1.1, no_symptom_no_cancer, bar_width, color="pink", label="No Symptom, No Cancer")
    plt.bar(x_axis + bar_width * 1.1, no_symptom_yes_cancer, bar_width, color="red", label="No Symptom, Cancer")

    # sets labels
    plt.xticks(x_axis + bar_width / 2, map(add_newlines, df.keys()), fontsize=8)
    plt.xlabel(x_label)
    plt.ylabel("Percent of Reponses")
    plt.title(f"Prevalence of Lung Cancer In Individuals With and Without Certain {x_label}")

    # shows figure
    plt.legend(loc="best")
    plt.savefig(f"lung-cancer/graphs/{x_label.lower()}.png")

if __name__ == "__main__":
    print(
        """
        1. Causes
        2. Symptoms
        """
    )
    method = input("Enter the type of variable you want to analyse: ")

    # check if method is invalid
    while method not in ["1", "2"]:
        method = input("Invalid method! Enter a valid choice: ")

    plot(method)
