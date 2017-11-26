import pickle
import pathlib

import pandas as pd


def unicoder(str):
    try:
        return unicode(str)
    except ValueError, TypeError:
        return u'invalid'


def get_data(test=False, unicoded=False):
    if not test:
        df_train = pd.read_csv('data/train_data.csv')
        df_train.drop(['is_duplicate'], axis=1, inplace=True)
        df_labels = pd.read_csv('data/train_labels.csv')
        df = df_train.merge(df_labels)
    else:
        df = pd.read_csv('data/test_data.csv')
    if unicoded:
        df.question1 = df.question1.apply(lambda x: unicoder(x))
        df.question2 = df.question2.apply(lambda x: unicoder(x))
        return df.loc[(df.question1 != 'invalid') | (df.question2 != 'invalid'), :]
    else:
        return df


def save_model(model, model_dir):
    model_dir = pathlib.Path(model_dir)
    weights = model.get_weights()
    if model_dir is not None:
        with (model_dir / 'model').open('wb') as file_:
            pickle.dump(weights[1:], file_)
        with (model_dir / 'config.json').open('wb') as file_:
            file_.write(model.to_json())