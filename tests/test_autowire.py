# -*- coding: utf-8 -*-

import unittest
from zope.interface import Interface
from zope.interface.verify import verifyObject


class IFoo(Interface):
    pass


class AutowireTestCase(unittest.TestCase):

    def test_interface(self):
        from pyramid_services_autowire import IAutowire, Autowire
        obj = Autowire()
        verifyObject(IAutowire, obj)

    def test_repr(self):
        from pyramid_services_autowire import Autowire
        obj = Autowire(IFoo, is_contextual=True, name='foo')
        self.assertIn('IFoo', repr(obj))
        self.assertIn('is_contextual=True', repr(obj))
        self.assertIn("name='foo'", repr(obj))
