import json
import logging
import os

import spacy
import numpy as np
import pandas as pd
from tqdm import tqdm

from helpers import get_data

tqdm.pandas(tqdm())
nlp = spacy.load('en')
nlp = spacy.load('en_core_web_lg')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Spacy
# ========
# ENTITY RECOGNITION
# nlp = spacy.load('en')
# doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')
#
# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)
#
# SIMILARITY
# nlp = spacy.load('en_core_web_lg')
# tokens = nlp(u'dog cat banana sasquatch')
#
# for token in tokens:
#     print(token.text, token.has_vector, token.vector_norm, token.is_oov)


# add similarity as a feature
def apply_similarity(str1, str2):
    if isinstance(str1, unicode) and isinstance(str2, unicode):
        return nlp(str1).similarity(nlp(str2))
    else:
        np.nan


def find_entities(str):
    entities = {}
    if isinstance(str, unicode):
        for token in nlp(unicode(str)).ents:
            if not token.label_ in entities:
                entities[token.label_] = 1
            else:
                entities[token.label_] += 1
        if len(entities) > 0:
            return entities
        else:
            return np.nan
    else:
        return np.nan


# ADD TO DATA
df = get_data(unicoded=True)
head = df.head(10000)
head['entities1'] = head.loc[:, 'question1'].progress_apply(lambda x: find_entities(x))
head['entities2'] = head.loc[:, 'question2'].progress_apply(lambda x: find_entities(x))
head['similarity_score'] = head.progress_apply(lambda row: apply_similarity(row['question1'], row['question2']), axis=1)
head.to_csv('data/head_with_sim_and_ents.csv')

head = pd.read_csv('data/head_with_sim_and_ents.csv')


# dummify entities from stored dicts
def rename_entitity_column(df, counter):
    logging.info(df.columns)
    for col in df.columns:
        if col in ENTS:
            new = '{}_{}'.format(col, counter)
            logging.info('renaming {} to {}'.format(col, new))
            df.rename(columns={'{}'.format(col): new}, inplace=True)
    return df


def string_to_dict(dict_string):
    # Convert to proper json format
    dict_string = dict_string.replace("'", '"').replace('u"', '"')
    return json.loads(dict_string)


ENTS = {u'CARDINAL', u'DATE', u'EVENT', u'FAC', u'GPE', u'LANGUAGE', u'LAW', u'LOC', u'MONEY', u'NORP', u'ORDINAL',
        u'ORG', u'PERCENT', u'PERSON', u'PRODUCT', u'QUANTITY', u'TIME', u'WORK_OF_ART'}

for row in train_df.loc[:, 'entities1']:
    if isinstance(row, dict):
        for k in row.keys():
            ENTS.add(k)


def get_features(dataframe):
    # get all unique entities
    dataframe.entities1 = dataframe.entities1.progress_apply(lambda x: string_to_dict(x) if isinstance(x, str) else np.nan)
    dataframe = pd.concat([dataframe, dataframe['entities1'].progress_apply(pd.Series).fillna(0)], axis=1)
    rename_entitity_column(dataframe, 1)
    dataframe.entities2 = dataframe.entities2.progress_apply(lambda x: string_to_dict(x) if isinstance(x, str) else np.nan)
    dataframe = pd.concat([dataframe, dataframe['entities2'].progress_apply(pd.Series).fillna(0)], axis=1)
    rename_entitity_column(dataframe, 2)
    return dataframe


# process in batches
BATCHSIZE = 1000
df = get_data(unicoded=True)
counter = 1
for batch in range(0, len(df), BATCHSIZE):
    end = batch+BATCHSIZE if batch+BATCHSIZE < len(df) else len(df)
    logging.info('Starting batch {} from {} to {}'.format(counter, batch, end))
    tdf = df.iloc[batch:batch+BATCHSIZE]
    tdf.question1 = tdf.question1.apply(lambda x: unicoder(x))
    tdf.question2 = tdf.question2.apply(lambda x: unicoder(x))
    tdf['entities1'] = tdf.loc[:, 'question1'].progress_apply(lambda x: find_entities(x))
    tdf['entities2'] = tdf.loc[:, 'question2'].progress_apply(lambda x: find_entities(x))
    tdf['similarity_score'] = tdf.progress_apply(lambda row: apply_similarity(row['question1'], row['question2']), axis=1)
    tdf.to_csv('batches/batch_{}.csv'.format(counter))
    counter += 1
logging.info('Finished {} batches'.format(counter))



# build train_set
train_df = get_data(unicoded=True)
for filename in os.listdir('batches'):
    if filename.endswith('.csv'):
        batch_df = pd.read_csv('batches/{}'.format(filename))
        train_df = train_df.merge(batch_df.loc[:, ['id', 'entities1', 'entities2', 'similarity_score']], on='id', how='left')
        if filename != 'batch_1.csv':
            train_df['entities1'] = train_df['entities1_y'].fillna(train_df['entities1_x'])
            train_df['entities2'] = train_df['entities2_y'].fillna(train_df['entities2_x'])
            train_df['similarity_score'] = train_df['similarity_score_y'].fillna(train_df['similarity_score_x'])
            train_df.drop(['entities1_x', 'entities1_y'], axis=1, inplace=True)
            train_df.drop(['entities2_x', 'entities2_y'], axis=1, inplace=True)
            train_df.drop(['similarity_score_x', 'similarity_score_y'], axis=1, inplace=True)
        logging.info('Merged in {}, new length {}'.format(filename, len(train_df.loc[train_df.similarity_score.isna() == False])))
        continue
    else:
        continue
final = get_features(train_df.loc[train_df.similarity_score.isna() == False])


# get test data
test = pd.read_csv('data/test_data.csv')
test.question1 = test.question1.apply(lambda x: unicoder(x))
test.question2 = test.question2.apply(lambda x: unicoder(x))
test['entities1'] = test.loc[:, 'question1'].progress_apply(lambda x: find_entities(x))
test['entities2'] = test.loc[:, 'question2'].progress_apply(lambda x: find_entities(x))
test['similarity_score'] = test.progress_apply(lambda row: apply_similarity(row['question1'], row['question2']), axis=1)
test.to_csv('data/test_with_sim_and_ents.csv')

test.entities1 = test.entities1.progress_apply(lambda x: string_to_dict(x) if isinstance(x, str) else np.nan)
test = pd.concat([test, test['entities1'].apply(pd.Series).fillna(0)], axis=1)
rename_entitity_column(test, 1)
test.entities2 = test.entities2.progress_apply(lambda x: string_to_dict(x) if isinstance(x, str) else np.nan)
test = pd.concat([test, test['entities2'].apply(pd.Series).fillna(0)], axis=1)
rename_entitity_column(test, 2)



# fit a classifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier()
train, test = train_test_split(b.drop(['id', 'question1', 'question2', 'entities1', 'entities2'], axis=1).fillna(0))
x_train = train.drop(['is_duplicate'], axis=1).values
x_test = test.drop(['is_duplicate'], axis=1).values
y_train = train.is_duplicate.values
y_test = test.is_duplicate.values

fit = forest.fit(x_train, y_train)
y_pred = forest.predict(x_test)
mean_squared_error(y_test, y_pred)
r2_score(y_test, y_pred)

final_test = pd.read_csv('data/test_with_sim_and_ents.csv')
final_test = get_features(final_test)
x_final = a.drop(['test_id', 'question1', 'question2', 'entities1', 'entities2'], axis=1).values
final_pred = forest.predict(x_final)
naive = pd.read_csv('naive_submission.csv')
naive['is_duplicate'] = final_pred
naive.to_csv('entity_class_test.csv', index=False)


from sklearn.linear_model import LogisticRegression
lm = LogisticRegression()
fitlm = lm.fit(x_train, y_train)
y_predlm = fitlm.predict(x_test)
mean_squared_error(y_test, y_pred)
r2_score(y_test, y_pred)

