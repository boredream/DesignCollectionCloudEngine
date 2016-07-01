# coding: utf-8

from leancloud import Engine
from leancloud import LeanEngineError
from main import scrapyexecute

from app import app

engine = Engine(app)


@engine.define
def scrapy(**params):
    scrapyexecute.start_scrapy()


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
