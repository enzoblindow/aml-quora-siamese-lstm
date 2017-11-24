import pandas as pd


def create_train_data():
    df_train = pd.read_csv('data/train_data.csv')
    df_train.drop(['is_duplicate'], axis=1, inplace=True)
    df_labels = pd.read_csv('data/train_labels.csv')
    return df_train.merge(df_labels)