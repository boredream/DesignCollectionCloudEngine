# coding=utf-8

import urllib2
import json
import sqlite3

count = 50

headers = {
    "X-LC-Id": "iaEH7ObIA4sPY8RSs3VCVXBg-gzGzoHsz",
    "X-LC-Key": "dXfhXIVyeWMN2czJkd4ehwzs",
    "Content-Type": "application/json"
}
url = "https://api.leancloud.cn/1/classes/DesignRes"
url_batch = "https://api.leancloud.cn/1/batch"
batch_request = {"requests": []}
column_names = []

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info("DATA")')
for column in cursor.fetchall():
    column_names.append(column[1])


def query(page=1):
    """查询"""
    limit = 20
    skip = (page - 1) * limit
    query_url = url + '?limit=%s&skip=%s' % (limit, skip)

    request = urllib2.Request(query_url, headers=headers)
    content = urllib2.urlopen(request).read()

    content_json = str(content)
    data = json.loads(content_json)
    return data['results']


def add():
    """添加"""

    # 先从数据库中查询未提交到服务器的数据
    print 'query local datas'
    cursor.execute("SELECT * FROM DATA WHERE isAdd = '0'")
    for item in cursor.fetchall():
        body = {}
        for index in range(0, len(item)):
            body[column_names[index]] = item[index]

        request = {
            "method": "POST",
            "path": "/1.1/classes/DesignRes",
            "body": body
        }
        batch_request['requests'].append(request)
        if len(batch_request['requests']) == count:
            break

    if len(batch_request['requests']) == 0:
        print 'no data need add'
        return

    data = json.dumps(batch_request)

    print 'add data 2 server'
    request = urllib2.Request(url_batch, headers=headers, data=data)
    content = urllib2.urlopen(request).read()

    # 更新成功，更新本地数据库
    if 'success' in str(content):
        print 'update local data add status~ after success'
        for item in batch_request['requests']:
            srcLink = item['body']['srcLink']
            sql_update = "update DATA set isAdd = '1' where srcLink = '%s'" % srcLink
            conn.execute(sql_update)

        conn.commit()
        print 'update local data success'
