from django.http import HttpResponse

class SampleOne(object):
    """A completely custom view handler.

    A view handler is any class that takes a request in its
    constructor and has a __call__ method that returns an
    HttpResponse.  Usually, you will store the request as an instance
    attribute of the handler class so that it can be accessed by other
    class methods.  Storing instance attributes is threadsafe because
    each request gets it's own instance of a handler class.

    By implementing part of the handler logic in the ``get_message``
    method, we provide a hook for customizing the handler through
    subclassing.  See SampleTwo for an example.

    You cannot use a handler class directly in a url configuration
    file.  It must be wrapped by a View class, which creates instances
    of the handler for each request.  The url conf that uses this
    handler looks like this:

        from django.conf.urls.defaults import patterns, url
        from paulo.sweetness import View
        from sampleapp import views

        urlpatterns = patterns(
            '',
            url(r'^one/$', View(views.SampleOne)),
        )
    """

    def __init__(self, request):
        self.request = request

    def get_message(self):
        echo = self.request.GET.get("echo", "nothing")
        return "This is a basic handler. You said: %s" % echo

    def __call__(self):
        return HttpResponse(self.get_message(),
                            content_type="text/plain")


class SampleOneWithParams(SampleOne):
    """A view handler that subclasses another.

    This handler subclasses SampleOne and so inherits all the
    functionality provided in SampleOne.  However, we override the
    constructor and the ``get_message`` method to provide additional
    functionality: the ability to pass a name as part of the url.

    In addition to a request, the constructor for a view handler can
    take additional arguments and keyword arguments.  These arguments
    will be extracted from the regex groups in a url config. The url
    regex for this handler looks like this: ^one/(.*)/$
    """

    def __init__(self, request, name):
        super(SampleOneWithParams, self).__init__(request)
        self.name = name

    def get_message(self):
        original = super(SampleOneWithParams, self).get_message()
        return "%s to %s" % (original, self.name)


from paulo.sweetness import BaseHandler

class SampleTwo(BaseHandler):
    """Using the BaseHandler helper class.

    Sweetness provides a BaseHandler class for subclassing.  The
    BaseHandler class provides a default constructor that makes the
    request available as an instance attribute.  More useful though is
    a class method which makes it easier to use a handler like a
    traditional Django view.

    The url conf for this handler looks like this:

        url(r'^two/$', views.SampleTwo.view)

    Like traditional Django views, you can just call the
    ``SampleTwo.view`` class method and get an HttpResponse back:

        response = SampleTwo.view(request)
    """

    def __call__(self):
        return HttpResponse("method: %s\nquery params:%r" % (self.request.method,
                                                             dict(self.request.GET)),
                            content_type="text/plain",)


from paulo.sweetness import Handler

class SampleThree(Handler):
    """Using the Handler base class.

    The ``Handler`` class provides a number of useful helpers that
    you'll see in the next few samples.

    In this sample, you see that the __call__ method is implemented
    for us by the ``Handler`` base class.  The __call__ method
    delegates to two other methods: ``update`` and ``render``.

    The ``update`` method is meant to prepare all the data needed for
    rendering.  This usually involves doing database queries and any
    business logic.

    The ``render`` method is then responsible for returning a fully
    rendered HttpResponse.  By seperating out the update and render
    methods into two seperate steps, it's easier to customize those
    sections.  For example, a subclass of ``SampleThree`` could change
    the render method to use an html template instead of inlined plain
    text by only overriding the render method.
    """

    def update(self):
        self.message = "Update happens before render!"

    def render(self):
        return HttpResponse("Render happens after update. "
                            "Here is another message: %s" % self.message,
                            content_type="text/plain")

class SampleFour(Handler):
    """Using a template with the Handler base class.

    The ``Handler`` base class actually implements a ``render`` method
    for you that uses a template specified as a class attribute.  That
    leaves the ``update`` method as the only implementation detail
    left.

    The Handler class also has a ``context`` dictionary that gets
    passed to the template.  In the ``update`` method below, we add
    the 'info' variable to the template context using the context
    dictionary.

    By default, templates also have access to the Handler instance
    that is rendering the template, this is passed in as the 'view'
    variable.  So in the template we would access the variables like
    so:

        {{info}} <!-- From the context dictionary of the Handler instance -->
        {{view.message}} <!-- view refers to the Handler instance itself -->
    """

    template = "sampleapp/four.html"

    def update(self):
        self.message = "Attributes of the handler are available to the template via view.*"
        self.context['info'] = "The handler can make other things available to the template"


from paulo.sweetness import fromurl

class SampleFive(Handler):
    """Extracting arguments from the url regex.

    Rather than retrieving url arguments as parameters passed to a
    function, we can specify a mapping from url regex groups to
    instance attributes.  This makes subclassing and customization
    easier as you do not have to change method signatures when your
    urls change.

    In thie sample we use positional arguments by passing the argument
    index to the ``fromurl`` helper function.  The urlconf looks like
    this:

        url(r'^five/(.*)/(.*)/$', views.SampleFive.view)

    """

    template = "sampleapp/five.html"

    arg1 = fromurl(0)
    arg2 = fromurl(1)


class SampleSix(Handler):
    """Extracting named regex groups from a url.

    We can also extract named regex groups by passing the name of the
    group to the fromurl helper function.  If no match is found, we
    can make a default value available.  The urlconf looks like this:

        url(r'^six/(?P<kwarg>.*)/(?P<blarg>.*)/$', views.SampleSix.view),

    """

    template = "sampleapp/six.html"

    kwarg = fromurl("kwarg")
    blarg = fromurl("blarg", default="{no blarg given}")


from sampleapp.models import BlogPost
from django.contrib.auth.models import User

class SampleSeven(Handler):
    """Looking up a model automatically.

    Information passed through url regex groups typically correspond
    to identifiers for models stored in the database.  We can have
    those models retrieved automatically for us.  In this sample are
    three examples of how to do that.

        fromurl("slug").model(BlogPost)

    corresponds to

        BlogPost.objects.get(slug="<slug group in regex>")

    and

        fromurl("other_slug").model(BlogPost, "slug")

    corresponds to

        BlogPost.objects.get(slug="<other_slug group in regex>")

    If the BlogPost.objects.get() calls raise ObjectDoesNotExist then
    a 404 response will be returned.  If you specify
    ``required=False`` then a 404 response will not be returned and
    the instance attribute will be set to None.
    """

    template = "sampleapp/seven.html"

    blog_post = fromurl("slug").model(BlogPost)
    other_post = fromurl("other_slug").model(BlogPost, "slug")
    user = fromurl("username").model(User, required=False)
