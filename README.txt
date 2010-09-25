=========
Sweetness
=========

About
-----

Sweetness is a micro framework for working with class based views in
Django.  It's goals are to be:

- **Lightweight**: should be able to fit into one file for easy use on
  google app engine.
- **Flexible**: should be easily made to work with different
  authentication systems and database models (including appengine
  models and authentication).
- **Easy**: should be easy to create class based views that can be
  extended and customized through inheritance rather than a million
  keyword arguments

Getting Started
---------------

You can get the development environment up and running with the
``bootstrap.py`` and ``buildout`` script.  This installs a local
encapsulated version of django with a sqlite database backend::

  $ python bootstrap.py
  $ ./bin/buildout

Once you have this setup, you should read over the sampleapp to see
how sweetness works.

Running the samples
-------------------

Running the samples is as easy as starting django::

  $ ./bin/django runserver

All the code for these samples is in the ``src/sampleapp/`` directory.

Key Concepts
------------

The View Class
..............

In Django, a view is typically written as a function that accepts a
request and some parameters, and then returns an HttpResponse.  In
sweetness, we use instances of the ``sweetness.View`` class as our
views.  ``sweetness.View`` implements the ``__call__`` method, so
instances of ``sweetness.View`` are therefore callable just like a
function.  Like a regular Django view function, the ``__call__``
method accepts a request and some parameters and returns an
HttpResponse.

The View Handler Class
......................

The ``sweetness.View`` class is one part of a two part solution to
class based views.  The other part is a View *Handler* class.  A view
handler class does all the heavy lifting that would otherwise be done
by a Django view function.  Each incoming request is handled by a
seperate instance of a Handler class, and a Handler class'
``__call__`` method is responsible for returning an HttpResponse.  A
Handler is instantiated by passing in a request and some parameters,
and when the Handler instance is called (via ``__call__``) an
HttpResponse is returned.

A Basic Example
...............

