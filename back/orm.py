import hashlib
import os
from pony.orm import *
from yamath.settings import EXPERIMENTAL_DATABASE_PATH


db = Database()


class User(db.Entity):
    email = PrimaryKey(str, 40)
    phash = Required(str, 32)
    status = Required(str, 4)
    legacyUsername = Optional(str, 40)
    firstName = Optional(unicode, 160)
    lastName = Optional(unicode, 160)
    isEditor = Optional(bool)
    isTeacher = Optional(bool)
    classrooms = Set('Classroom')
    means = Set('Mean')
    receiveds = Set('Envelope', reverse='receiver')
    sents = Set('Envelope', reverse='sender')


class Classroom(db.Entity):
    name = PrimaryKey(unicode, 160)
    topics = Set('Topic')
    users = Set('User')


class Node(db.Entity):
    name = PrimaryKey(unicode, 160)
    bloom = Optional(str, 10, nullable=True, default='remember')
    mobile = Optional(bool, default=True)
    notes = Optional(LongUnicode, default="No notes to this node")
    text = Optional(LongUnicode, default="No text to this node")
    antes = Set('Node', reverse='posts')
    means = Set('Mean')
    posts = Set('Node', reverse='antes')
    questions = Set('Question')
    topics = Set('Topic')


class Question(db.Entity):
    id = PrimaryKey(int, auto=True)
    kind = Required(str, 10, default='open')
    options = Required(Json, nullable=True)
    text = Required(LongUnicode, default="No text to this question")
    name = Optional(unicode, 160, nullable=True, default="No name to this question")
    notes = Optional(LongUnicode, default="No notes to this question")
    node = Optional('Node')


class Topic(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(unicode, 160, default="Undefined topic")
    notes = Optional(LongUnicode, default="No notes on this topic")
    text = Optional(LongUnicode, default="No text to this topic")
    antes = Set('Topic', reverse='posts')
    classrooms = Set('Classroom')
    nodes = Set('Node')
    posts = Set('Topic', reverse='antes')


class Mean(db.Entity):
    id = PrimaryKey(int, auto=True)
    node = Required('Node')
    history = Required(str, 8, default='XXXXXXXX')
    user = Required('User')


class Envelope(db.Entity):
    id = PrimaryKey(int, auto=True)
    sender = Required(User, reverse='sents')
    receiver = Required(User, reverse='receiveds')
    name = Optional(unicode, 160)
    notes = Optional(LongUnicode, default="No notes to this envelope")
    read = Optional(bool, default=False)
    text = Optional(LongUnicode, default="No text to this envelope")


os.remove(EXPERIMENTAL_DATABASE_PATH)
db.bind("sqlite", EXPERIMENTAL_DATABASE_PATH, create_db=True)
db.generate_mapping(create_tables=True)

def addNodeAnteNode(ante, post):
    with db_session:
        Node[ante].posts.add(Node[post])

def addUserInClassroom(email, name):
    with db_session:
        Classroom[name].users.add(User[email])

def add(model, field, kwargs, other_model, other_kwargs):
    with db_session:
        getattr(eval(model).get(**kwargs), field).add(eval(other_model).get(**other_kwargs))

def delete(model, pk=None, _lambda=None, **kwargs):
    with db_session:
        if model in ['User', 'Classroom', 'Node', 'Question', 'Topic', 'Mean', 'Envelope']:
            if pk:
                eval(model)[pk].delete()
            elif _lambda:
                eval(model).select(_lambda).delete()
            elif kwargs:
                eval(model).get(**kwargs).delete()
        else:
            raise KeyError(model)

def get(model, pk=None, **kwargs):
    with db_session:
        print('db get', kwargs)
        if model in ['User', 'Classroom', 'Node', 'Question', 'Topic', 'Mean', 'Envelope']:
            if 'pplain' in kwargs:
                kwargs['phash'] = hashlib.shake_128(kwargs['pplain'].encode()).hexdigest(16)
                del kwargs['pplain']        
            if pk:
                return eval(model)[pk]
            elif kwargs:
                return eval(model).get(**kwargs)
        else:
            raise KeyError(model)

#def getRelList(instance, relation):
#    with db_session:
#        return list(getattr(instance.__class__[instance.get_pk()], relation))

def new(model, **kwargs):
    with db_session:
        print('db new', model, kwargs)
        if model in ['User', 'Classroom', 'Node', 'Question', 'Topic', 'Mean', 'Envelope']:
            if 'pplain' in kwargs:
                kwargs['phash'] = hashlib.shake_128(kwargs['pplain'].encode()).hexdigest(16)
                del kwargs['pplain']  
            newInstance = eval(model)(**kwargs)
            return newInstance
        else:
            raise KeyError(model)

def removeUserInClassroom(email, name):
    with db_session:
        Classroom[name].users.remove(User[email])
    
def select(model, _lambda=lambda i: True):
    with db_session:
        if model in ['User', 'Classroom', 'Node', 'Question', 'Topic', 'Mean', 'Envelope']:
            return list(eval(model).select(_lambda))
        else:
            raise KeyError(model)

def update(model, pk, **kwargs):
    with db_session:
        if model in ['User', 'Classroom', 'Node', 'Question', 'Topic', 'Mean', 'Envelope']:
            if 'pplain' in kwargs:
                user = User[pk]
                user.phash = hashlib.shake_128(kwargs['pplain'].encode()).hexdigest(16)
                del kwargs['pplain']
            eval(model)[pk].set(**kwargs)
        else:
            raise KeyError(model)