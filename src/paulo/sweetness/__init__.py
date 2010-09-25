import inspect
import types
import logging

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import Http404


class View(object):
    '''A callable view that delegates to a handler.
    '''
    def __init__(self, handler_factory):
        self.handler_factory = handler_factory

    @property
    def __name__(self):
        return self.handler_factory.__name__

    def __call__(self, request, *args, **kwargs):
        try:
            handler = self.handler_factory(request, *args, **kwargs)
        except TypeError, e:
            logging.error("Failed to instantiate handler using factory %r",
                          self.handler_factory)
            raise
        return handler()


class BaseHandler(object):
    '''A very basic handler with helper methods'''

    def __init__(self, request):
        self.request = request

    @classmethod
    def view(cls, request, *args, **kwargs):
        return View(cls)(request, *args, **kwargs)


class Handler(BaseHandler):
    '''A handler for use with a callable view.'''

    template = None
    login_required = False

    def check_wrapper(self, wrapper):
        '''Test a security wrapping decorator (like login_required).

        Will return None if the decorator has no effect, otherwise
        returns the response the decorator returns.
        '''
        return wrapper(lambda request: None)(self.request)

    def check_permission(self):
        '''Ensures that the user has permission to access this handler.

        if permission is granted, nothing will be returned.  If
        permission is not granted, an HttpResponse will be returned
        pointing the user to an authentication screen if applicable.
        '''
        if self.login_required:
            return self.check_wrapper(login_required)

    def __init__(self, request, *args, **kwargs):
        super(Handler, self).__init__(request)
        self.context = {}
        for key, prop in inspect.getmembers(self.__class__):
            if isinstance(prop, UrlGroupProperty):
                value = prop.get_value(request, args, kwargs)
                setattr(self, key, prop.get_value(request, args, kwargs))
                if prop.add_to_context:
                    self.context[key] = value

    def update(self, *args, **kwargs):
        pass

    def render(self):
        if not self.template:
            raise NotImplementedError("Subclasses must implement a render method or specify a template.")

        self.context.setdefault('view',self)
        return render_to_response(self.template, self.context,
                                  context_instance=RequestContext(self.request))

    def __call__(self):
        response = self.check_permission()
        if response:
            return response
        response = self.update()
        if response:
            return response
        return self.render()


class UrlGroupProperty(object):
    """Property of a class that is automatically populated by url parameters."""

    def __init__(self, lookup, default=None, factory=None, add_to_context=False):
        self.lookup = lookup
        self.default = default
        self.factory = factory
        self.add_to_context = add_to_context

    def get_value(self, request, args, kwargs):
        if isinstance(self.lookup, types.StringTypes):
            result = kwargs.get(self.lookup, self.default) or self.default
        elif isinstance(self.lookup, types.IntType):
            result = args[self.lookup]
        if self.factory is not None:
            result = self.factory(result)
        return result

    def fromurl(self, lookup):
        """Return a new url property that gets its value from the specified regex group"""
        return UrlGroupProperty(lookup,
                                default=self.default,
                                factory=self.factory,
                                add_to_context=self.add_to_context)

    def model(self, model_class, field=None, required=True):
        """Return a new property that retreives a model based on a url regex group.

        If a model cannot be looked up and required is set to True,
        then a 404 error will be raised.
        """
        field = field or self.lookup
        def factory(url_value):
            try:
                return model_class.objects.get(**{field:url_value})
            except models.ObjectDoesNotExist, e:
                if required:
                    raise Http404("No match for %s=%r" % (field, url_value))
                return None

        return UrlGroupProperty(self.lookup,
                                default=self.default,
                                factory=factory,
                                add_to_context=self.add_to_context)


def fromurl(*args, **kwargs):
    return UrlGroupProperty(*args, **kwargs)
