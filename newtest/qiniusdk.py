# -*- coding:utf-8 -*-

from newtest import app
from qiniu import Auth,put_stream,put_file
import os

access_key = app.config['QINIU_ACCESS_KEY']
secrt_key = app.config['QINIU_SECRET_KEY']

q = Auth(access_key, secrt_key)

bucket_name = app.config['QINIU_BUCKET_NAME']
save_dir = app.config['UPLOAD_DIR']

def qiniu_upload_file(source_file,save_file_name):
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, save_file_name)

    ret, info = put_file(token, save_file_name, 
        os.path.join(save_dir,save_file_name))

    print type(info.status_code), info
    
    return None

