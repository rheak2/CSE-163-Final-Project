'''
docstring
'''

import utils
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from Species_Data_Processing.py import process_big_data
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import seaborn as sns
import matplotlib.pyplot as plt

sns.set()

def manipulate_data(data:pd.DataFrame) -> pd.DataFrame:
    data = utils.extinction_level_numerical(data)
    data = utils.tl_change_between_multiple_yrs(2007, 2021, data)
    return data


def train_and_test_model(data: pd.DataFrame) -> pd.DataFrame:

    # Separate data into features and labels
    # features = data.loc[:, ['Common name', 'location']]
    features = data.loc[:, ['Common name']]
    features = pd.get_dummies(features)
    labels = data['Average TL Change Over Time']

    # Breaks the data into 80% train and 20% test
    features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.2)

    # Create an untrained model
    model = DecisionTreeRegressor()

    # Train it on the **training set**
    model.fit(features_train, labels_train)

    # Compute training accuracy
    train_predictions = model.predict(features_train)
    train_error = mean_squared_error(labels_train, train_predictions)

    # Compute test accuracy
    test_predictions = model.predict(features_test)
    test_error = mean_squared_error(labels_test, test_predictions)

    data['Train Predictions'] = pd.Series(train_predictions)
    data['Test Predictions'] = pd.Series(test_predictions)

    return data


def plot_change_over_time(df: pd.DataFrame):
    '''
    given the training predictions, plot the change as a line plot between 2021-2035.
    '''
    avg_pred_train_by_type = df.groupby('Class')['Train Predictions'].mean()
    avg_pred_test_by_type = df.groupby('Class')['Test Predictions'].mean()
    avg_start_tl_by_type = df.groupby('Class')('IUCN Red List (2007) Category').mean()
    test_and_train_df = avg_pred_train_by_type.merge(avg_pred_test_by_type, left_on='Class', right_on='Class')
    pred_and_tl_df = test_and_train_df.merge(avg_start_tl_by_type, left_on='Class', right_on='Class')
    pred_and_tl_df.loc[:, 'Predicted TL 2035 Category'] = pred_and_tl_df.loc[:, 'IUCN Red List (2007) Category'] - 2 * pred_and_tl_df.loc[:, 'IUCN Red List (2007) Category']
    
    sns.relplot(data=pred_and_tl_df, x='')
    plt.title("Class Exctinction Threat Levels 2021-2035")
    plt.xlabel("Year")
    plt.ylabel("Threat Level")
    plt.savefig("Threat Levels by Class 2021-2035.png", bbox_inches="tight")


def do_question_3():
    csv_file = process_big_data('/Users/elizabethkaras/Desktop/Table_7_2007-2021')

    df = manipulate_data(df)
    output = train_and_test_model(df)
    plot_change_over_time(output)
