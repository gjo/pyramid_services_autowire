.. -*- coding: utf-8 -*-

=========================
pyramid_services_autowire
=========================

An autowire utility for `pyramid_services`.


before::

  class IService(Interface):
      pass

  class Service(object):
      def __init__(self, dep_svc1=None, dep_svc2=None, dep_svc3=None):
          self.dep_svc1 = dep_svc1
          self.dep_svc2 = dep_svc2
          self.dep_svc3 = dep_svc3

  def includeme(config):
      config.include('pyramid_services')
      def factory(context, request):
          svc = Service(
              dep_svc1=request.find_service(IDependService1),
              dep_svc2=request.find_service(IDependService2),
              dep_svc3=request.find_service(IDependService3),
          )
          return svc
      config.register_service_factory(factory, IService)


after::

  from pyramid_services_autowire import Autowire

  class IService(Interface):
      pass

  class Service(object):
      dep_svc1 = Autowire(IDependService1)
      dep_svc2 = Autowire(IDependService2)
      dep_svc3 = Autowire(IDependService3)

  def includeme(config):
      config.include('pyramid_services_autowire')
      config.register_autowire(Service, IService)
