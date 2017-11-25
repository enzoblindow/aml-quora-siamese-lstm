import spacy
import numpy as np
import pandas as pd
from tqdm import tqdm
import json

from helpers import get_data

tqdm.pandas(tqdm())
nlp = spacy.load('en')
nlp = spacy.load('en_core_web_lg')


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

# get all unique entities
ents = set()
for row in head.loc[:,'entities1']:
    if isinstance(row, dict):
        for k in row.keys():
            ents.add(k)


# dummify entities from stored dicts
def rename_entitity_column(df, entity_set, counter):
    for col in df.columns:
        if col in entity_set:
            df.rename(columns={'{}'.format(col): '{}_{}'.format(col, counter)}, inplace=True)

def string_to_dict(dict_string):
    # Convert to proper json format
    dict_string = dict_string.replace("'", '"').replace('u"', '"')
    return json.loads(dict_string)

head.entities1 = head.entities1.progress_apply(lambda x: string_to_dict(x) if isinstance(x, str) else np.nan)
head = pd.concat([head, head['entities1'].apply(pd.Series).fillna(0)], axis=1)
rename_entitity_column(head, ents, 1)
head.entities2 = head.entities2.progress_apply(lambda x: string_to_dict(x) if isinstance(x, str) else np.nan)
head = pd.concat([head, head['entities2'].apply(pd.Series).fillna(0)], axis=1)
rename_entitity_column(head, ents, 2)



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
rename_entitity_column(test, ents, 1)
test.entities2 = test.entities2.progress_apply(lambda x: string_to_dict(x) if isinstance(x, str) else np.nan)
test = pd.concat([test, test['entities2'].apply(pd.Series).fillna(0)], axis=1)
rename_entitity_column(test, ents, 2)


# fit a classifier
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier()
x = head.drop(['is_duplicate', 'question1', 'question2', 'entities1', 'entities2'], axis=1).fillna(0).values
y = head.is_duplicate.values

x_test = test.drop(['question1', 'question2', 'entities1', 'entities2'], axis=1).fillna(0).values
fit = forest.fit(x,y)
forest.predict_proba(x_test)