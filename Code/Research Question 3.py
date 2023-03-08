'''
docstring
'''

import utils
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
import species_data_processing_file
from sklearn.model_selection import train_test_split

sns.set()

def manipulate_data(data:pd.DataFrame) -> pd.DataFrame:
    data = utils.extinction_level_numerical(data)
    data = utils.tl_change_between_multiple_yrs(2007, 2021, data)
    return data

def train_and_test_model(data: pd.DataFrame) -> Any:

    # Separate data into features and labels
    features = data.loc[:, ['Common name', 'location']]
    features = pd.get_dummies(features)
    labels = data['Average TL Change Over Time']

    # Breaks the data into 80% train and 20% test
    features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size=0.2)

    # Create an untrained model
    model = DecisionTreeClassifier()

    # Train it on the **training set**
    model.fit(features_train, labels_train)

    # Compute training accuracy
    train_predictions = model.predict(features_train)
    train_accuracy = accuracy_score(labels_train, train_predictions)

    # Compute test accuracy
    test_predictions = model.predict(features_test)
    test_accuracy = accuracy_score(labels_test, test_predictions)

    output = [train_predictions, train_accuracy, test_predictions, test_accuracy]

def plot_change_over_time(model_output: list[Any]):
    '''
    given the training predictions, plot the change as a line plot between 2021-2035.
    '''
    sns.relplot(data=class_threat_level_by_year_df.T, kind="line")
    plt.title("Class Exctinction Threat Levels 2021-2035")
    plt.xlabel("Year")
    plt.ylabel("Threat Level")
    plt.savefig("Threat Levels by Class 2021-2035.png", bbox_inches="tight")



def main():
    df = species_data_df
    df = manipulate_data(df)




if __name__ == "__main__":
   main()