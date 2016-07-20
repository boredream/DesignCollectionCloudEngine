# coding: utf-8

from leancloud import Object
from leancloud import Query
from leancloud import LeanCloudError
from flask import Blueprint
from flask import render_template


class DesignRes(Object):
    pass


todos_view = Blueprint('reslist', __name__)


@todos_view.route('')
def show():
    try:
        datas = Query(DesignRes).descending('createdAt').find()
    except LeanCloudError, e:
        if e.code == 101:  # 服务端对应的 Class 还没创建
            datas = []
        else:
            raise e
    return render_template('reslist.html', datas=datas)
