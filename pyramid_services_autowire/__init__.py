# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from zope.interface import Interface


__version__ = '0.1.1'
__license__ = 'MIT'


class DoesNotWired(Exception):
    pass


class Autowire(object):
    def __init__(self, iface=None, is_contextual=None, name=None,
                 name_property=None):
        self.iface = iface
        self.is_contextual = is_contextual
        self.name = name
        self.name_property = name_property

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        raise DoesNotWired(self.iface)


def register_autowire(config, cls, iface=Interface, context=Interface, name='',
                      **kwargs):
    fields = {k: v for k, v in cls.__dict__.items() if isinstance(v, Autowire)}

    def factory(ctxt, req):
        obj = cls(**kwargs)
        for k, v in fields.items():
            if k not in obj.__dict__:
                params = {}
                if v.iface:
                    params['iface'] = v.iface
                if v.is_contextual:
                    params['context'] = ctxt
                if v.name:
                    params['name'] = v.name
                elif v.name_property:
                    params['name'] = getattr(obj, v.name_property)
                svc = req.find_service(**params)
                setattr(obj, k, svc)
        return obj

    config.register_service_factory(factory, iface, context, name)


def includeme(config):
    config.include('pyramid_services')
    config.add_directive('register_autowire', register_autowire)
