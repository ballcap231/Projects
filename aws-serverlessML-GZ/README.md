# serverless-machine-learning
This repo deployed support vector regression model for house prices predictions, a ResNet50 model for top-3 image classification, and pre-trained SpaCy model for textual entities and dependencies visualization to AWS Lambda with Serverless framework and Python 3. This repo was done as part of a Udemy Course. Installation packages were not uploaded as part of this repo.

## Contents
### hello-world
Hello World example of creating a project with Serverless and deploying to AWS Lambda in Python.

### scikit-example
An example of Serverless project which contains machine learning regression model from scikit-learn trained on California housing dataset.

### spacy-example
An example of Serverless project which uses a small English model from spaCy NLP framework to create an AWS Lambda endpoint for named entity recognition.

### spacy-assignment
An example of Serverless project which uses a small English model from spaCy NLP framework to create an AWS Lambda endpoint for parts of speech tagging and dependency parsing.

### keras-example
An example of Serverless project which uses ResNet50 computer vision deep learning model from Keras framework to create an AWS Lambda endpoint for image recognition. The example requires two S3 buckets (one for model storage and other for image uploads) and optional AWS Identity Pool configuration.

### keras-assignment
An example very similar to above keras-example, but uses InceptionV3 model instead of ResNet50. This was not implemented in this repo.

### web-gui-code
Contains a web page for sending requests to endpoints created with above examples. Endpoints, URLs and other credentials were added to `js/app.js` file.
