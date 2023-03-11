'''
docstring
'''

import utils
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from process_table_7.py import process_big_data
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

    print("The MSE between the train predictions and the true values is ", train_error)
    print("The MSE between the test predictions and the true values is ", test_error)

    return data


def plot_change_over_time(df: pd.DataFrame) -> None:
    '''
    given the training predictions, plot the change as a line plot between 2021-2035.
    '''
    avg_pred_train_by_type = df.groupby('Class')['Train Predictions'].mean()
    avg_pred_test_by_type = df.groupby('Class')['Test Predictions'].mean()
    plot_predictions(avg_pred_train_by_type, 'Average Change Over Time By Class Based on Training Predictions', 'Avg Change in TL by Class (train)')
    plot_predictions(avg_pred_test_by_type, 'Average Change Over Time By Class Based on Training Predictions', 'Avg Change in TL by Class (test)')



def plot_predictions(data_df: pd.DataFrame, graph_title: str, img_title: str) -> None:
    '''
    ...
    '''
    sns.catplot(data=data_df, x='Class', y='Train Predictions')
    plt.title(graph_title)
    plt.xlabel("Class")
    plt.ylabel("Average Change in Threat Level")
    plt.savefig(img_title, bbox_inches="tight")


def do_question_3():
    df = process_big_data('Table_7_Loc_Data')
    df = manipulate_data(df)
    df_with_predictions = train_and_test_model(df)
    plot_change_over_time(df_with_predictions)
