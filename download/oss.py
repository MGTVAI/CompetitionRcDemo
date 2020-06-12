# -*- coding: utf-8 -*-

import oss2
import logging
import json
import sys
import base64
from itertools import islice

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format=FORMAT)


def get_oss_file(param):
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
    bucket_obj.get_object_to_file(
        "mgtv_contest/resb/recommendation/recommendation/eval.tar.gz", "./eval.tar.gz")
    bucket_obj.get_object_to_file(
        "mgtv_contest/resb/recommendation/recommendation/train.tar.gz", "./train.tar.gz")


def main():
    if len(sys.argv) != 2:
        logging.error("please run with : python oss.py <code>")
        sys.exit(1)
    obj = json.loads(base64.b64decode(sys.argv[1]))
    get_oss_file(obj)


if __name__ == "__main__":
    main()
