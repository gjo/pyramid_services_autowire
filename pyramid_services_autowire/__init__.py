# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from zope.interface import Attribute, Interface, implementer


__version__ = '0.2.dev1'
__license__ = 'MIT'


class DoesNotWired(AttributeError):
    pass


class IAutowire(Interface):
    iface = Attribute('Interface of service')
    is_contextual = Attribute('use context when service locating')
    name = Attribute('Name of service')
    name_property = Attribute('Property name of name of service')


@implementer(IAutowire)
class Autowire(object):
    def __init__(self, iface=None, is_contextual=None, name=None,
                 name_property=None):
        self.iface = iface
        self.is_contextual = is_contextual
        self.name = name
        self.name_property = name_property

    def __repr__(self):
        return '<Autowire({})>'.format(', '.join([
            '{}={}'.format(k, repr(v)) for k, v in self.__dict__.items() if v
        ]))

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        raise DoesNotWired(obj, self)


def register_autowire(config, cls, iface=Interface, context=Interface, name='',
                      **kwargs):
    fields = {k: v for k, v in cls.__dict__.items() if IAutowire.providedBy(v)}

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
