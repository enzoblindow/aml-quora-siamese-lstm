# Quora Question Pairs

## Project Description
Where else but Quora can a physicist help a chef with a math problem and get cooking tips in return? Quora is a place to gain and share knowledge—about anything. It’s a platform to ask questions and connect with people who contribute unique insights and quality answers. This empowers people to learn from each other and to better understand the world.

Over 100 million people visit Quora every month, so it's no surprise that many people ask similarly worded questions. Multiple questions with the same intent can cause seekers to spend more time finding the best answer to their question, and make writers feel they need to answer multiple versions of the same question. Quora values canonical questions because they provide a better experience to active seekers and writers, and offer more value to both of these groups in the long term.

Currently, Quora uses a Random Forest model to identify duplicate questions. In this competition, Kagglers are challenged to tackle this natural language processing problem by applying advanced techniques to classify whether question pairs are duplicates or not. Doing so will make it easier to find high quality answers to questions resulting in an improved experience for Quora writers, seekers, and readers.

Acknowledgements

Data and descriptions modified from https://www.kaggle.com/c/quora-question-pairs

## Evaluation

Submissions are evaluated on the category accuracy between the predicted label (0 or 1) and the truth label (0 or 1). 1 means duplicate and 0 otherwise. The formula is then,

![loss](http://chart.apis.google.com/chart?cht=tx&chf=bg,s,FFFFFF00&chl=CategoryAccuracy=\frac{1}{N}\sum{1}_{y_i=\hat{y}_i})

where N is the number of question pairs in the test set, yiyi is the true label for the i-th question pair, and ŷ iy^i is the predicted label.

Submission File

For each question pair in the test set, you must predict whether the questions are duplicates. The file should contain a header and have the following format:

### Submission Format

You must submit a csv file with the image name, all candidate class names, and a probability for each class. The order of the rows does not matter. The file must have a header and should look like the following:

```
test_id,is_duplicate
0,1
1,1
2,1
...
etc.
```
