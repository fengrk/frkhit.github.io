---
layout: post
title: tornado文件上传服务
category: 技术
tags: tornado
keywords: 
description: 
---

# tornado文件上传服务

代码例子:

```
import tornado.ioloop
import tornado.web
import os
import json
import tempfile


class FileUploadHandler(tornado.web.RequestHandler):
    """
        ref: https://blog.csdn.net/dutsoft/article/details/53942983
        author: dutsoft
    """
    def get(self):
        self.write('''
<html>
  <head><title>Upload File</title></head>
  <body>
    <form action='file' enctype="multipart/form-data" method='post'>
    <input type='file' name='file'/><br/>
    <input type='submit' value='submit'/>
    </form>
  </body>
</html>
''')

    def post(self):
        result = {'result': 'OK'}
        file_metas = self.request.files.get('file', None)

        if not file_metas:
            result['result'] = 'Invalid Args'
            return result

        # prepare upload path
        upload_path = os.path.join(tempfile.gettempdir(), 'files')
        if not os.path.exists(upload_path):
            os.mkdir(upload_path)

        # save upload file in local disk
        for meta in file_metas:
            filename = meta['filename']
            file_path = os.path.join(upload_path, filename)
            print("file_path is {}, file_name is {}".format(file_path, filename))

            with open(file_path, 'wb') as up:
                up.write(meta['body'])

        self.write(json.dumps(result))


app = tornado.web.Application([
    (r'/file', FileUploadHandler),
])

if __name__ == '__main__':
    app.listen(8080)
    tornado.ioloop.IOLoop.instance().start()

```
