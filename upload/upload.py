#!/bin/env python
# -*- coding: utf-8 -*-

import oss2
import logging
import os
import json
import sys
import base64

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)


def get_oss_file(param, local_file):
    endpoint = 'oss-cn-beijing.aliyuncs.com'
    bucket = 'video-match'
    auth = oss2.StsAuth(
        param.get('id'),
        param.get('secret'),
        param.get('stoken'),
    )
    bucket_obj = oss2.Bucket(auth, endpoint, bucket)
    '''
    here we just known the file path, can be change  to your self path , or just list the bucket
    '''
    key = param.get('osspath')[18:] + os.path.basename(local_file)
    with open(local_file) as f:
        bucket_obj.put_object(key, f)
        logging.info("put %s success", local_file)


def main():
    if len(sys.argv) != 3:
        logging.error(
            "please run with : python oss.py <local_file_path> <code>")
        sys.exit(1)
        assert(os.path.isfile(sys.argv[1]))
        assert(len(sys.argv[2]) > 10)
    obj = json.loads(base64.b64decode(sys.argv[2]))
    get_oss_file(obj, sys.argv[1])


if __name__ == "__main__":
    main()
