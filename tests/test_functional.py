# -*- coding: utf-8 -*-

import unittest
from pyramid.config import Configurator
from pyramid.request import Request
from zope.interface import Interface, implementer


class FunctionalTestCase(unittest.TestCase):

    def test_does_not_wired(self):
        from pyramid_services_autowire import Autowire, DoesNotWired
        class IDepSvc(Interface):
            pass

        class Svc(object):
            dep_svc = Autowire(IDepSvc)

        self.assertIsInstance(Svc.dep_svc, Autowire)
        svc = Svc()
        self.assertRaises(DoesNotWired, getattr, svc, 'dep_svc')

    def test_by_iface(self):
        from pyramid_services_autowire import Autowire

        class ISvc(Interface):
            pass

        class IDepSvc(Interface):
            pass

        class Svc(object):
            dep_svc = Autowire(IDepSvc)

        config = Configurator()
        config.include('pyramid_services_autowire')

        dep_svc = object()
        config.register_autowire(Svc, ISvc)
        config.register_service(dep_svc, IDepSvc)

        def aview(request):
            svc = request.find_service(ISvc)
            self.assertIsInstance(svc, Svc)
            self.assertIs(svc.dep_svc, dep_svc)
            return request.response

        config.add_route('root', pattern='/')
        config.add_view(aview, route_name='root')
        app = config.make_wsgi_app()
        resp = Request.blank('/').get_response(app)
        self.assertEqual(resp.status_code, 200)

    def test_by_contextual(self):
        from pyramid_services_autowire import Autowire

        class IRoot(Interface):
            pass

        class ISome(Interface):
            pass

        @implementer(ISome)
        class Some(object):
            def __init__(self, parent, name):
                self.__parent__ = parent
                self.__name__ = name

        @implementer(IRoot)
        class Root(dict):
            def __init__(self, request):
                super(Root, self).__init__()
                self['some'] = Some(self, 'some')

        class ISvc(Interface):
            pass

        class IDepSvc(Interface):
            pass

        class Svc(object):
            dep_svc = Autowire(IDepSvc, is_contextual=True)

        config = Configurator(root_factory=Root)
        config.include('pyramid_services_autowire')

        dep_svc_root = object()
        dep_svc_some = object()
        config.register_autowire(Svc, ISvc)
        config.register_service(dep_svc_root, IDepSvc, context=IRoot)
        config.register_service(dep_svc_some, IDepSvc, context=ISome)

        def root_view(request):
            svc = request.find_service(ISvc)
            self.assertIsInstance(svc, Svc)
            self.assertIs(svc.dep_svc, dep_svc_root)
            return request.response

        def some_view(request):
            svc = request.find_service(ISvc)
            self.assertIsInstance(svc, Svc)
            self.assertIs(svc.dep_svc, dep_svc_some)
            return request.response

        config.add_view(root_view, context=IRoot)
        config.add_view(some_view, context=ISome)
        app = config.make_wsgi_app()
        resp = Request.blank('/').get_response(app)
        self.assertEqual(resp.status_code, 200)
        resp = Request.blank('/some/').get_response(app)
        self.assertEqual(resp.status_code, 200)

    def test_by_name(self):
        from pyramid_services_autowire import Autowire

        class ISvc(Interface):
            pass

        class Svc(object):
            dep_svc = Autowire(name='foo')

        config = Configurator()
        config.include('pyramid_services_autowire')

        dep_svc = object()
        config.register_autowire(Svc, ISvc)
        config.register_service(dep_svc, name='foo')

        def aview(request):
            svc = request.find_service(ISvc)
            self.assertIsInstance(svc, Svc)
            self.assertIs(svc.dep_svc, dep_svc)
            return request.response

        config.add_route('root', pattern='/')
        config.add_view(aview, route_name='root')
        app = config.make_wsgi_app()
        resp = Request.blank('/').get_response(app)
        self.assertEqual(resp.status_code, 200)

    def test_by_name_property(self):
        from pyramid_services_autowire import Autowire

        class ISvc(Interface):
            pass

        class Svc(object):
            dep_svc = Autowire(name_property='foo')

            def __init__(self, foo=None):
                self.foo = foo

        config = Configurator()
        config.include('pyramid_services_autowire')

        dep_svc = object()
        config.register_autowire(Svc, ISvc, foo='foo')
        config.register_service(dep_svc, name='foo')

        def aview(request):
            svc = request.find_service(ISvc)
            self.assertIsInstance(svc, Svc)
            self.assertIs(svc.dep_svc, dep_svc)
            return request.response

        config.add_route('root', pattern='/')
        config.add_view(aview, route_name='root')
        app = config.make_wsgi_app()
        resp = Request.blank('/').get_response(app)
        self.assertEqual(resp.status_code, 200)
