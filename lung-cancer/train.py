import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from visualize import SYMPTOMS, CAUSES

# convert gender to number
def gender_mapper(gender): return 1 if gender == "M" else 0

# demographics which may be helpful in prediction
DEMOGRAPHICS = ["GENDER", "AGE"]

# model types to test
MODELS = ["random_forest", "naive_bayes", "svc"]

# reads data from the csv file
df = pd.read_csv("lung-cancer/data/lung-cancer.csv", usecols=SYMPTOMS+CAUSES)

# changes 2's to 1's and 1's to 0's - convert to binary for yes and no
for stat in df:
    df[stat] = df[stat] - 1

# get demographic data
demo_df = pd.read_csv("lung-cancer/data/lung-cancer.csv", usecols=DEMOGRAPHICS)
for stat in demo_df:
    if stat == "GENDER":    # set males to 1, females to 0
        df[stat] = list(map(gender_mapper, demo_df[stat]))
    else:
        df[stat] = demo_df[stat]

# gets if they have cancer or not
results = pd.read_csv("lung-cancer/data/lung-cancer.csv", usecols=["LUNG_CANCER"])["LUNG_CANCER"]

# split into train and test
train_x, test_x, train_y, test_y = train_test_split(df, results)

# create models
random_forest = RandomForestClassifier(random_state=101, n_estimators=100)
naive_bayes = MultinomialNB()
svc = SVC()

# train and test models
for name in MODELS:

    # gets model based on what the string is
    model  = eval(name)
    model.fit(train_x, train_y)

    # test model accuracy
    predicted_y = model.predict(test_x)
    accuracy = accuracy_score(test_y, predicted_y)

    print(f"The accuracy of the {name} model is {round(100 * accuracy, 2)}%.")