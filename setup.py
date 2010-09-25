from setuptools import setup, find_packages
import os

setup(
    name = "paulo.sweetness",
    version = "0.1.0",
    license = 'LGPL 2',
    description = "Mini Class-based views framework for django",
    author = 'Paul Carduner',
    author_email = 'paul@carduner.net',
    packages = ['paulo.sweetness'],
    package_dir = {'': 'src'},
    namespace_packages = ['paulo'],
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
