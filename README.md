# aml-kaggle

## Project Description
Plankton are critically important to our ecosystem, accounting for more than half the primary productivity on earth and nearly half the total carbon fixed in the global carbon cycle. They form the foundation of aquatic food webs including those of large, important fisheries. Loss of plankton populations could result in ecological upheaval as well as negative societal impacts, particularly in indigenous cultures and the developing world. Plankton’s global significance makes their population levels an ideal measure of the health of the world’s oceans and ecosystems.

Traditional methods for measuring and monitoring plankton populations are time consuming and cannot scale to the granularity or scope necessary for large-scale studies. Improved approaches are needed. One such approach is through the use of an underwater imagery sensor. This towed, underwater camera system captures microscopic, high-resolution images over large study areas. The images can then be analyzed to assess species populations and distributions.

Manual analysis of the imagery is infeasible – it would take a year or more to manually analyze the imagery volume captured in a single day. Automated image classification using machine learning tools is an alternative to the manual approach. Analytics will allow analysis at speeds and scales previously thought impossible. The automated system will have broad applications for assessment of ocean and ecosystem health.

The National Data Science Bowl challenges you to build an algorithm to automate the image identification process. Scientists at the Hatfield Marine Science Center and beyond will use the algorithms you create to study marine food webs, fisheries, ocean conservation, and more. This is your chance to contribute to the health of the world’s oceans, one plankton at a time.

Acknowledgements

The National Data Science Bowl is presented by with data provided by the Hatfield Marine Science Center at Oregon State University.

Acknowledgements

Data and descriptions modified from https://www.kaggle.com/c/datasciencebowl

## Evaluation

Submissions are evaluated using the multi-class logarithmic loss. Each image has been labeled with one true class. For each image, you must submit a set of predicted probabilities (one for every class). The formula is then,

![loss](http://chart.apis.google.com/chart?cht=tx&chf=bg,s,FFFFFF00&chl=logloss=-\frac{1}{N}\sum_{i=1}^N\sum_{j=1}^My_{ij}\log(p_{ij}))

where N is the number of images in the test set, M is the number of class labels, log is the natural logarithm, yijyij is 1 if observation i is in class j and 0 otherwise, and pijpij is the predicted probability that observation i belongs to class j.

The submitted probabilities for a given image are not required to sum to one because they are rescaled prior to being scored (each row is divided by the row sum). In order to avoid the extremes of the log function, predicted probabilities are replaced with max(min(p,1−10−15),10−15)max(min(p,1−10−15),10−15).

### Submission Format

You must submit a csv file with the image name, all candidate class names, and a probability for each class. The order of the rows does not matter. The file must have a header and should look like the following:

```
image,acantharia_protist_big_center,...,unknown_unclassified
1.jpg,0.00826446,...,0.00826446
10.jpg,0.00826446,...,0.00826446
...
etc
```
