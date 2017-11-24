import spacy
import numpy as np
from tqdm import tqdm, tqdm_pandas

from helpers import create_train_data

tqdm.pandas(tqdm())
nlp = spacy.load('en')
nlp = spacy.load('en_core_web_lg')


# ENTITY RECOGNITION
doc = nlp(u'Apple is looking at buying U.K. startup for $1 billion')

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)

# SIMILARITY
tokens = nlp(u'dog cat banana sasquatch')

for token in tokens:
    print(token.text, token.has_vector, token.vector_norm, token.is_oov)


# add similarity as a feature
def apply_similarity(str1, str2):
    if isinstance(str1, unicode) and isinstance(str2, unicode):
        return nlp(str1).similarity(nlp(str2))
    else:
        np.nan


def find_entities(str):
    # print('finding entitites for: {}'.format(str))
    entities = {}
    if isinstance(str, unicode):
        for token in nlp(unicode(str)).ents:
            if not token.label_ in entities:
                entities[token.label_] = 1
            else:
                entities[token.label_] += 1
        if len(entities) > 0:
            # print('found: {}'.format(entities))
            return entities
        else:
            return np.nan
    else:
        return np.nan


# ADD TO DATA
df = create_train_data(unicoded=True)
head = df.head(10000)
head['entities1'] = head.loc[:, 'question1'].progress_apply(lambda x: find_entities(x))
head['similarity_score'] = head.progress_apply(lambda row: apply_similarity(row['question1'], row['question2']), axis=1)
head.to_csv('data/head_with_sim_and_ents.csv')