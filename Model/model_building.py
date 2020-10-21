from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import pickle
import time
import os


def read_data():
    path = 'cleaned_data.csv'
    data = pd.read_csv(path)
    return data

def process(data, mms=None, fit=False):
    if fit and mms:
        return mms.transform(data)
    elif not fit:
        mms = MinMaxScaler()
        scaled_data = mms.fit_transform(data)
        return scaled_data, mms
    else:
        raise "CheckScalerError"

def run_process_tasks():    
    df = read_data()
    X = df.drop(['seu'], axis=1)
    y = df['seu']

    print('Preprocessing data...')
    tic = time.time()
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    X_train, Scaler = process(X_train, True)
    X_test = process(X_test, Scaler)
    toc = time.time()
    print('Task done in {:.3f} second(s)'.format(toc-tic))

    print("Saving scaler")
    pickle.dump(Scaler, open(os.path.join('Model', 'scaler.pkl'), 'wb'))
    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    rfc = RandomForestClassifier(class_weight='balanced')
    params = {'n_estimators' : [80, 90, 100, 110],
              'max_depth' : [2, 3, 4, 5]
             }
    clf = RandomizedSearchCV(rfc, params, scoring='balanced_accuracy')

    print('Training model with cross validation...')
    tic = time.time()
    search = clf.fit(X_train, y_train)
    toc = time.time()
    print('Task done in {:.3f} second(s)'.format(toc-tic))

    model = search.best_estimator_
    print('Best score was found to be {:.3f}'.format(search.best_score_))
    print('Best params were {}'.format(search.best_params_))

    print('Saving model')
    pickle.dump(model, open(os.path.join('Model', 'model.pkl'), 'wb'))

X_train, X_test, y_train, y_test = run_process_tasks()
train_model(X_train, y_train)