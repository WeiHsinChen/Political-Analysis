import os
import sys
import string
import csv
from time import time
import numpy as np

# scikit
from sklearn import datasets
from sklearn.pipeline import Pipeline
from sklearn.base import TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2

# model
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib

# error report
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# nltk 
import nltk
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer 


class SentimentAnalysis:
  """

  SentimentAnalysis module is used to analyze the sentiment of tweets

  """
  def __init__(self):
    """
    Construct a new 'SentimentAnalysis' object.
    """
    self.clf = None

  def parse_training_dataset(self, train_path):
    """ 
    Process a raw training dataset, e.g. tokenization and lemmatization.

    :param train_path: the path of a raw training dataset
    """
    print 
    print 'parsing...'
    start = time()

    # variables
    train_data = []
    train_label = []
    dev_data = []
    dev_label = []
    puncSet = set(string.punctuation)
    stemmer = SnowballStemmer("english")
    wordnet_lemmatizer = WordNetLemmatizer()

    # tokenize and stem with lower case
    count = 0
    for line in open(train_path, 'r'):
      """
      save raw data to sklearn
      """
      tmp = line.split(',')
      train_label.append(int(tmp[0].strip()[1:-1]))
      content = nltk.word_tokenize(tmp[5].strip().decode('iso-8859-1')[1:-1])
      tmp_data = ""
      for w in content:
        # if w not in puncSet:
        tmp_data += " " + wordnet_lemmatizer.lemmatize(w.lower())
        # tmp_data += " " + stemmer.stem(w.lower())
      train_data.append(tmp_data[1:])
    train_label = np.array(train_label)
    # save data and label
    train_data_file = open('train_data', 'wb+')
    train_label_file = open('train_label', 'wb+')
    np.save(train_data_file, train_data)
    np.save(train_label_file, train_label)
    train_data_file.close()
    train_label_file.close()

    print "parsing: cost %f sec" % (time()-start)
    return (train_data, train_label)

  def train_model(self, train_data, train_label):
    """ 
    Save an already trained model

    :param train_data: the path of a processed dataset 
    :param train_label: the path of a label dataset for the processed dataset
    """
    print 
    print 'training...'
    start = time()

    num_feature = len(train_data[0])
    clf_tmp = Pipeline([('vect', CountVectorizer(ngram_range=(1,3))), 
        ('tfidf', TfidfTransformer(use_idf=True)),
        # ('feaSel',  SelectKBest(chi2, k=12000000)),
        # ('feaSel',  SelectKBest(chi2, k=num_feature*0.7)),
        # ('clf', LinearSVC())])
        ('clf', MultinomialNB())])

    self.clf = clf_tmp.fit(train_data, train_label)
    train_predict = self.clf.predict(train_data)

    print classification_report(train_label, train_predict)
    print confusion_matrix(train_label, train_predict)
    print

    print "training: cost %f sec" % (time()-start)

  def save_model(self, model_output_path):
    """ 
    Save an already trained model

    :param model_output_path: the path of a model for analysis
    """
    print 
    print 'saving model...'
    start = time()

    joblib.dump(self.clf, model_output_path) 

    print "saving model: cost %f sec" % (time()-start)

  def load_model(self, model_input_path):
    """ 
    Load an already trained model

    :param model_input_path: the path of a model for analysis
    """
    print 
    print 'loading model...'
    start = time()
    # if self.clf == None:
    #   self.train('./datasets/train.csv', model_output_path=model_input_path, processed=True, save=True)
    self.clf = joblib.load(model_input_path) 

    print "loading model: cost %f sec" % (time()-start)

  def load_train_data(self):
    """ 
    Load an already processed training dataset
    """
    print 
    print 'loading...'
    start = time()

    train_data_path = './datasets/train_data'
    train_label_path = './datasets/train_label'
    tmp1 = np.load(train_data_path)
    tmp2 = np.load(train_label_path)

    print "loading data: cost %f sec" % (time()-start)
    return (tmp1, tmp2)

  def train(self, train_path, model_output_path='', processed=False, save=False):
    """ 
    Train the model for sentiment analysis.

    :param train_path: the path of a training dataset
    :param model_output_path: the path of the output model
    :param processed: does it need to re-process training dataset or not
    :param save: does it need to save the model or not
    """
    if processed:
      (train_data, train_label) = self.load_train_data()
    else:
      (train_data, train_label) = self.parse_training_dataset(train_path)
    self.train_model(list(train_data), train_label)
    if save:
      self.save_model(model_output_path)

  def test_data(self, test_path, output_path):
    """ 
    Predict sentiment of a bunch of tweets.

    :param test_path: the path of a test dataset
    :param output_path: the path of output file 
    """
    print 
    print 'testing...'
    start = time()

    test_data = []
    test_label = []
    test_id = []
    puncSet = set(string.punctuation)
    stemmer = SnowballStemmer("english")
    wordnet_lemmatizer = WordNetLemmatizer()
    count_vect = CountVectorizer()
    # count_vect = CountVectorizer(tokenizer=LemmaTokenizer())
    tfidf_transformer = TfidfTransformer()

    # tokenize and stem with lower case
    for line in open(test_path, 'r'):
      tmp = line.split(',')
      # parse test id
      tmp[0] = tmp[0].strip()
      if tmp[0][0] == '"':
        tmp[0] = tmp[0][1:]
      if tmp[0][-1] == '"':
        tmp[0] = tmp[0][:-1]

      test_id.append(tmp[0])  
      # test_label.append(int(tmp[0].strip()[1:-1]))
      content = nltk.word_tokenize(tmp[4].strip().decode('iso-8859-1')[1:-1])
      tmp_data = ""
      for w in content:
        # if w not in puncSet:
        # tmp_data += " " +stemmer.stem(w.lower())
        tmp_data += " " +wordnet_lemmatizer.lemmatize(w.lower())
      test_data.append(tmp_data[1:])
        
    # output
    output_file = open(output_path, 'wb+')
    writer = csv.writer(output_file)
    writer.writerow(['ID', 'Predicted_label'])
    for tid, pred in zip(test_id, self.clf.predict(test_data)):
      writer.writerow([tid, pred])
    output_file.close()

    print "testing data: cost %f sec" % (time()-start)

  def predict_sentiment(self, text):
    """ 
    Predict sentiment of a new tweet.

    :param text: The text of the tweet
    :return: The sentiment of the tweet, 4 means positive and 0 means negative
    """
    return self.clf.predict([text])[0]


# sa = SentimentAnalysis()
# sa.train('./datasets/train.csv', model_output_path='model_NB.pkl', processed=False, save=True)
