# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError

from app import app
from main import spiderexecute
from cloudspider import borespider

engine = Engine(app)


@engine.define
def spider(**params):
    tag = params.get('tag')
    if not tag:
        tag = borespider.ui_china_tag
    borespider.execute(tag)


@engine.define
def query(**params):
    if 'p' in params:
        spiderexecute.query(params['p'])
    spiderexecute.query(1)


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

# if __name__ == '__main__':
#     add()
