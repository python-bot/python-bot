#!/usr/bin/env python3

from distutils.core import setup
from setuptools import find_packages

setup(
    name='python_bot',
    version="0.1b0",
    url='https://github.com/python-bot/python-bot',
    author='Sergey Kovalev',
    author_email='44sergey@gmail.com',
    description='This library provides a pure Python interface for the Messenger Bot API',
    license='LGPL-3',
    include_package_data=True,
    scripts=[],
    install_requires=[],
    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: PythonBot',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: LGPL-3 License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
