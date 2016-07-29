# coding: utf-8

from flask import Blueprint
from flask import render_template
from main import spiderexecute

reslist_view = Blueprint('reslist', __name__)


@reslist_view.route('')
def show():
    datas = spiderexecute.query()
    return render_template('reslist.html', datas=datas)
