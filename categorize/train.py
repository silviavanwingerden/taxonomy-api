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

stemmer = SnowballStemmer("dutch")
vectorizer = CountVectorizer(analyzer="word", tokenizer=None,
                             preprocessor=None, stop_words=None,
                              max_features=800)
clean_train_tasks = joblib.load('/Users/Silvia/Sites/afstuderen/metadata/joblib/clean_train_tasks.pkl')
vectorizer.fit_transform(clean_train_tasks)


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
    joblib.dump(forest, '/Users/Silvia/Sites/afstuderen/metadata/joblib/forest.pkl')


def get_train_data_features(training):
    clean_train_tasks = []
    print training.shape
    for introduction in training["introduction"]:
        clean_train_tasks.append(task_to_words(introduction))
    print clean_train_tasks
    joblib.dump(clean_train_tasks, '/Users/Silvia/Sites/afstuderen/metadata/joblib/clean_train_tasks.pkl')

    # clean_train_tasks = joblib.load('../joblib/clean_train_tasks.pkl')
    train_data_features = vectorizer.fit_transform(clean_train_tasks)
    train_data_features = train_data_features.toarray()
    joblib.dump(train_data_features, '/Users/Silvia/Sites/afstuderen/metadata/joblib/train_data_features.pkl')

    train_forest(train_data_features, training)


def get_accuracy(test):
    clean_test_tasks = []
    for introduction in test["introduction"]:
        clean_test_tasks.append(task_to_words(introduction))
    joblib.dump(clean_test_tasks, '/Users/Silvia/Sites/afstuderen/metadata/joblib/clean_test_tasks.pkl')

    clean_train_tasks = joblib.load('/Users/Silvia/Sites/afstuderen/metadata/joblib/clean_train_tasks.pkl')
    train_data_features = vectorizer.fit_transform(clean_train_tasks)

    test_data_features = vectorizer.transform(clean_test_tasks)
    test_data_features = test_data_features.toarray()
    joblib.dump(test_data_features, '/Users/Silvia/Sites/afstuderen/metadata/joblib/test_data_features.pkl')

    forest = joblib.load('/Users/Silvia/Sites/afstuderen/metadata/joblib/forest.pkl')
    result = forest.predict(test_data_features)

    output = pandas.DataFrame(data={"introduction": test["introduction"], "category": result})
    print output


    precision = accuracy_score(test['question_type_id'], output['category'])
    return precision


def predict_single(text):
    array = []
    array.append(text)
    single = pandas.DataFrame({'introduction': array})
    #array voor 1 item?

    clean_task = []
    for introduction in single["introduction"]:
        clean_task.append(task_to_words(introduction))

    single_data_feature = vectorizer.transform(clean_task)
    single_data_feature = single_data_feature.toarray()

    forest = joblib.load('/Users/Silvia/Sites/afstuderen/metadata/joblib/forest.pkl')
    #waarom forest en niet nb

    result = forest.predict(single_data_feature)
    return str(result[0])

# read csv and split in test and training set


data = pandas.read_csv("/Users/Silvia/Sites/afstuderen/metadata/data/allquestiontypes.csv", header=0, delimiter=",")
data = data.dropna(subset=["introduction"])
training, test = train_test_split(data, test_size=0.2, random_state=12)

# print predict_single("leg uit waarom dit zo is")
# get_train_data_features(training)
# print get_accuracy(test)
