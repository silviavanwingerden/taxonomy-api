from bs4 import BeautifulSoup
import pandas
# Import the stop word list
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB
import joblib
import numpy
from sklearn.metrics import confusion_matrix, accuracy_score
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from sklearn import metrics
import re

stemmer = SnowballStemmer("dutch")


def getvectorizer():
    vectorizer = CountVectorizer(analyzer="word", tokenizer=None,
                                 preprocessor=None, stop_words=None,
                                  max_features=800)
    clean_train_tasks = joblib.load('/Users/Silvia/Sites/afstuderen/taxonomy-api/joblib/clean_train_tasks.pkl')
    vectorizer.fit_transform(clean_train_tasks)
    return vectorizer


def task_to_words(raw_task):
    review_text = BeautifulSoup(raw_task, 'lxml').get_text()
    letters_only = re.sub("[^a-zA-Z]", " ", review_text)
    words = letters_only.lower().split()
    # stops = set(stopwords.words("dutch"))
    # meaningful_words = [w for w in words if w not in stops]
    stemmed = []
    for savedword in words:
        stemmedword = stemmer.stem(savedword)
        stemmed.append(stemmedword)
    return(" ".join(stemmed))


def train_forest(train_data_features, training):
    forest = BernoulliNB()
    forest = forest.fit(train_data_features, training["question_type_id"])
    joblib.dump(forest, '/Users/Silvia/Sites/afstuderen/taxonomy-api/joblib/forest.pkl')


def get_train_data_features(training):
    clean_train_tasks = []
    for introduction in training["introduction"]:
        clean_train_tasks.append(task_to_words(introduction))
    joblib.dump(clean_train_tasks, '/Users/Silvia/Sites/afstuderen/taxonomy-api/joblib/clean_train_tasks.pkl')

    # clean_train_tasks = joblib.load('../joblib/clean_train_tasks.pkl')
    vectorizer = getvectorizer()
    train_data_features = vectorizer.fit_transform(clean_train_tasks)
    train_data_features = train_data_features.toarray()
    joblib.dump(train_data_features, '/Users/Silvia/Sites/afstuderen/taxonomy-api/joblib/train_data_features.pkl')

    train_forest(train_data_features, training)


data = pandas.read_csv("/Users/Silvia/Sites/afstuderen/taxonomy-api/data/allquestiontypes.csv", header=0, delimiter=",")
data = data.dropna(subset=["introduction"])
training, test = train_test_split(data, test_size=0.2, random_state=12)

get_train_data_features(training)
