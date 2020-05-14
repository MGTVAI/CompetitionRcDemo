#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: tangye <tangye@mgtv.com|tangyel@126.com>
# @author: zzh <zhouzhou@mgtv.com>


import fire
import pandas as pd
import pyarrow.parquet as pq


def load_data(file_path):
    """
    """
    table = pq.read_table(file_path)
    df = table.to_pandas()
    # TODO: here use your own feature engineering

    Y = df.pop('label').values
    return df, Y


def load_eval_data(file_path):
    table = pq.read_table(file_path)
    df = table.to_pandas()
    # TODO: here use your own feature engineering

    return df


if __name__ == '__main__':
    fire.Fire()
