# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError

from app import app
from main import spiderexecute
from cloudspider import borespider
from lxml import etree

engine = Engine(app)


@engine.define
def spider(**params):
    borespider.execute()


@engine.define
def query(**params):
    spiderexecute.query()


@engine.define
def add(**params):
    spiderexecute.add()


@engine.define
def hello(**params):
    print 'hello ~~~~~~~~~ there ~~~~~~~~~~~~~ '
    if 'name' in params:
        return 'Hello, {}!'.format(params['name'])
    else:
        return 'Hello, LeanCloud!'


@engine.before_save('Todo')
def before_todo_save(todo):
    content = todo.get('content')
    if not content:
        raise LeanEngineError('内容不能为空')
    if len(content) >= 240:
        todo.set('content', content[:240] + ' ...')
