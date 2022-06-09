#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @file: metrics.py

import numpy as np
from collections import defaultdict
from sklearn.metrics import roc_auc_score


def gauc(labels, preds, uids):
    """Calculate group auc
    :param labels: list
    :param predict: list
    :param uids: list
    >>> gauc([1,1,0,0,1], [0, 0,1,0,1], ['a', 'a','a', 'b', 'b'])
    0.4
    >>> gauc([1,1,0,0,1], [1,1,0,0,1], ['a', 'a','a', 'b', 'b'])
    1.0
    >>> gauc([1,1,1,0,0], [1,1,0,0,1], ['a', 'a','a', 'b', 'b'])
    0.0
    >>> gauc([1,1,1,0,1], [1,1,0,0,1], ['a', 'a','a', 'b', 'b'])
    1.0
    """
    assert len(uids) == len(labels)
    assert len(uids) == len(preds)
    group_score = defaultdict(lambda: [])
    group_truth = defaultdict(lambda: [])
    for idx, truth in enumerate(labels):
        uid = uids[idx]
        group_score[uid].append(preds[idx])
        group_truth[uid].append(truth)

    total_auc = 0
    impression_total = 0
    for user_id in group_truth:
        if label_with_xor(group_truth[user_id]):
            auc = roc_auc_score(np.asarray(
                group_truth[user_id]), np.asarray(group_score[user_id]))
            total_auc += auc * len(group_truth[user_id])
            impression_total += len(group_truth[user_id])
    group_auc = (float(total_auc) /
                 impression_total) if impression_total else 0
    group_auc = round(group_auc, 6)
    return group_auc


def label_with_xor(lists):
    """
    >>> label_with_xor([1,1,1])
    False
    >>> label_with_xor([0,0,0])
    False
    >>> label_with_xor([0,])
    False
    >>> label_with_xor([1,])
    False
    >>> label_with_xor([0,1])
    True
    """
    if not lists:
        return False
    first = lists[0]
    for i in range(1, len(lists)):
        if lists[i] != first:
            return True
    return False


def auc(y_true, y_score):
    '''
    :param y_true: shape = [n_samples] or [n_samples, n_classes]
    :param y_score: shape = [n_samples] or [n_samples, n_classes]
    :return:
    '''
    return roc_auc_score(y_true, y_score)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)

# vim: set tabstop=4 softtabstop=4 shiftwidth=4 noexpandtab
