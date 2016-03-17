from weakref import WeakKeyDictionary
from threading import currentThread
import importlib

from cloudshell.shell.core.context import InitCommandContext

CONTEXT_CONTAINER = WeakKeyDictionary()


def put_context(context):
    CONTEXT_CONTAINER[currentThread()] = build_suitable_context(context)


def get_context():
    if currentThread() in CONTEXT_CONTAINER:
        return CONTEXT_CONTAINER[currentThread()]
    return None


def build_suitable_context(context):
    module = importlib.import_module(InitCommandContext.__module__)
    context_class = str(context.__class__).split('.')[-1]
    if context_class in dir(module):
        classobject = getattr(module, context_class)
    else:
        raise Exception('build_suitable_context', 'Cannot find suitable class')
    obj = classobject()
    for attribute in filter(lambda x: not str(x).startswith('__') and not x == 'ATTRIBUTE_MAP', dir(context)):
        value = getattr(context, attribute)
        if value and str(value.__class__).split('.')[-1] in dir(module):
            value = build_suitable_context(value)

        if attribute in obj.ATTRIBUTE_MAP:
            obj_attr = obj.ATTRIBUTE_MAP[attribute]
        else:
            obj_attr = attribute

        setattr(obj, obj_attr, value)
    return obj


def context(func):
    def wrap_func(*args, **kwargs):
        put_context(args[0])
        return func(*args, **kwargs)

    return wrap_func
