# Data Description

The goal of this competition is to predict which of the provided pairs of questions contain two questions with the same meaning. The ground truth is the set of labels that have been supplied by human experts. The ground truth labels are inherently subjective, as the true meaning of sentences can never be known with certainty. Human labeling is also a 'noisy' process, and reasonable people will disagree. As a result, the ground truth labels on this dataset should be taken to be 'informed' but not 100% accurate, and may include incorrect labeling. We believe the labels, on the whole, to represent a reasonable consensus, but this may often not be true on a case by case basis for individual items in the dataset.

Please note: as an anti-cheating measure, Kaggle has supplemented the test set with computer-generated question pairs. Those rows do not come from Quora, and are not counted in the scoring. All of the questions in the training set are genuine examples from Quora.

## Files

**train_data.csv** - the training data file
**test_data.csv** - the test data file
**train_labels.csv** - the training labels file
**my_sample_submission.csv** - provides the appropriate format for generating a valid submission.


### Data fields

**id** - the id of a training set question pair
**question1, question2** - the full text of each question
**is_duplicate** - the target variable, set to 1 if question1 and question2 have essentially the same meaning, and 0 otherwise