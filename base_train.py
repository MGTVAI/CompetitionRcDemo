#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: tangye <tangye@mgtv.com|tangyel@126.com>
# @author: zzh <zhouzhou@mgtv.com|hzhzh007@gmail.com>

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import FeatureHasher
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.utils import parallel_backend
import pandas as pd
import metrics
import data_helper

from joblib import dump, load
from absl import flags, app
import traceback
import logging
import sys

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)

FLAGS = flags.FLAGS
flags.DEFINE_string('train_file', "",
                    'train input parquet path')
flags.DEFINE_string('test_file', ".",
                    'test input parquet path')
flags.DEFINE_string('submission_input_file', "",
                    'submission input parquet path')

flags.DEFINE_string('model_out', "./data/ouput/model.pkl", 'model checkpoint')
flags.DEFINE_string('test_out', "./data/ouput/test.data",
                    'test result output file')
flags.DEFINE_string('submission_out', "./data/ouput/submission.csv",
                    'submission result output file')


def lr(preprocessor, X, Y):
    # some model param
    n_jobs = 24
    C = 1.0
    penalty = 'l2'
    tol = 0.0001
    solver = 'lbfgs'
    class_weight = None
    verbose = 1
    max_iter = 100
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', LogisticRegression(C=C, penalty=penalty, tol=tol, verbose=verbose,
                                                            solver=solver, class_weight=class_weight, n_jobs=n_jobs, max_iter=max_iter))])
    clf.fit(X, Y)
    return clf


def test(test_out_filename, clf, test_df, y_true):
    y_prob = clf.predict_proba(test_df)
    y_score = y_prob[:, 1]
    uids = test_df['did'].values

    with open(test_out_filename, 'w') as e_out:
        auc = metrics.auc(y_true, y_score)
        e_out.write("auc: %s\n" % str(auc))
        logging.info("auc: %s", str(auc))
        gauc = metrics.gauc(y_true, y_score, uids)
        # e_out.write("ndcg: %s\n" % str(ndcg))
        e_out.write("gauc: %s\n" % str(gauc))
        logging.info("gauc: %s", str(gauc))


def submission_data(out_file_name, clf, submission_df):
    y_prob = clf.predict_proba(submission_df)
    output_df = submission_df[['index', ]].copy()
    output_df['score'] = y_prob[:, 1]
    output_df.to_csv(out_file_name, index=False, sep=',', header=True)
    logging.info("submission data write to:%s", FLAGS.submission_out)


def pipeline():
    '''
    '''
    # load files
    train_df, y_train = data_helper.load_data(FLAGS.train_file)
    logging.debug("train shape:%s,dtypes:%s",
                  train_df.shape, train_df.dtypes)

    # feature fit & transform
    categorical_features = ['mod', 'mf', 'aver', 'sver', 'vid', 'prev', ]
    categorical_transformer = Pipeline(
        steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[('cat', categorical_transformer, categorical_features), ])

    clf = lr(preprocessor, train_df, y_train)

    # model out
    try:
        dump(clf, FLAGS.model_out, compress=1)
    except:
        traceback.print_exc()

    # test
    if FLAGS.test_file:
        test_df, y_test = data_helper.load_data(FLAGS.test_file)
        test(FLAGS.test_out, clf, test_df, y_test)

    # submission
    if FLAGS.submission_input_file:
        submission_df = data_helper.load_eval_data(FLAGS.submission_input_file)
        submission_df = pd.DataFrame(submission_df, columns=test_df.columns)
        submission_data(FLAGS.submission_out, clf, submission_df)


def main(argv):
    with parallel_backend('threading'):
        pipeline()


if __name__ == '__main__':
    app.run(main)

# vim: set tabstop=4 softtabstop=4 shiftwidth=4 noexpandtab
