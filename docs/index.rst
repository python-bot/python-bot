.. Python bot documentation master file, created by
   sphinx-quickstart on Fri Jul 29 17:19:27 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python bot's documentation!
======================================

====================
Django documentation
====================

.. rubric:: Everything you need to know about Django.

Getting help
============

Having trouble? We'd like to help!

* Try the :doc:`FAQ <faq/index>` -- it's got answers to many common questions.

* Looking for specific information? Try the :ref:`genindex`, :ref:`modindex` or
  the :doc:`detailed table of contents <contents>`.


How the documentation is organized
==================================

Django has a lot of documentation. A high-level overview of how it's organized
will help you know where to look for certain things:

* :doc:`Tutorials </intro/index>` take you by the hand through a series of
  steps to create a Web application. Start here if you're new to Django or Web
  application development. Also look at the ":ref:`index-first-steps`" below.

* :doc:`Topic guides </topics/index>` discuss key topics and concepts at a
  fairly high level and provide useful background information and explanation.

* :doc:`Reference guides </ref/index>` contain technical reference for APIs and
  other aspects of Django's machinery. They describe how it works and how to
  use it but assume that you have a basic understanding of key concepts.

* :doc:`How-to guides </howto/index>` are recipes. They guide you through the
  steps involved in addressing key problems and use-cases. They are more
  advanced than tutorials and assume some knowledge of how Django works.

.. _index-first-steps:

First steps
===========

Are you new to Django or to programming? This is the place to start!

* **From scratch:**
  :doc:`Overview <intro/overview>` |
  :doc:`Installation <intro/install>`

* **Tutorial:**
  :doc:`Part 1: Requests and responses <intro/tutorial01>` |
  :doc:`Part 2: Models and the admin site <intro/tutorial02>` |
  :doc:`Part 3: Views and templates <intro/tutorial03>`

* **Advanced Tutorials:**
  :doc:`How to write reusable apps <intro/reusable-apps>` |
  :doc:`Writing your first patch for Django <intro/contributing>`

The model layer
===============

Django provides an abstraction layer (the "models") for structuring and
manipulating the data of your Web application. Learn more about it below:

* **Models:**
  :doc:`Introduction to models <topics/db/models>` |
  :doc:`Field types <ref/models/fields>` |
  :doc:`Indexes <ref/models/indexes>` |
  :doc:`Meta options <ref/models/options>` |
  :doc:`Model class <ref/models/class>`

* **The basics:**
  :doc:`URLconfs <topics/http/urls>` |
  :doc:`View functions <topics/http/views>` |
  :doc:`Shortcuts <topics/http/shortcuts>` |
  :doc:`Decorators <topics/http/decorators>`

* **Model instances:**
  :doc:`Instance methods <ref/models/instances>` |
  :doc:`Accessing related objects <ref/models/relations>`

* **Migrations:**
  :doc:`Introduction to Migrations<topics/migrations>` |
  :doc:`Operations reference <ref/migration-operations>` |
  :doc:`SchemaEditor <ref/schema-editor>` |
  :doc:`Writing migrations <howto/writing-migrations>`

* **Advanced:**
  :doc:`Managers <topics/db/managers>` |
  :doc:`Raw SQL <topics/db/sql>` |
  :doc:`Transactions <topics/db/transactions>` |
  :doc:`Aggregation <topics/db/aggregation>` |
  :doc:`Search <topics/db/search>` |
  :doc:`Custom fields <howto/custom-model-fields>` |
  :doc:`Multiple databases <topics/db/multi-db>` |
  :doc:`Custom lookups <howto/custom-lookups>` |
  :doc:`Query Expressions <ref/models/expressions>` |
  :doc:`Conditional Expressions <ref/models/conditional-expressions>` |
  :doc:`Database Functions <ref/models/database-functions>`

* **Other:**
  :doc:`Supported databases <ref/databases>` |
  :doc:`Legacy databases <howto/legacy-databases>` |
  :doc:`Providing initial data <howto/initial-data>` |
  :doc:`Optimize database access <topics/db/optimization>` |
  :doc:`PostgreSQL specific features <ref/contrib/postgres/index>`

* **For designers:**
  :doc:`Language overview <ref/templates/language>` |
  :doc:`Built-in tags and filters <ref/templates/builtins>` |
  :doc:`Humanization <ref/contrib/humanize>`

* **For programmers:**
  :doc:`Template API <ref/templates/api>` |
  :doc:`Custom tags and filters <howto/custom-template-tags>`


Internationalization and localization
=====================================

Django offers a robust internationalization and localization framework to
assist you in the development of applications for multiple languages and world
regions:

* :doc:`Overview <topics/i18n/index>` |
  :doc:`Internationalization <topics/i18n/translation>` |
  :ref:`Localization <how-to-create-language-files>` |
  :doc:`Localized Web UI formatting and form input <topics/i18n/formatting>`
* :doc:`Time zones </topics/i18n/timezones>`

Performance and optimization
============================

There are a variety of techniques and tools that can help get your code running
more efficiently - faster, and using fewer system resources.

* :doc:`Performance and optimization overview <topics/performance>`

Python compatibility
====================

Django aims to be compatible with multiple different flavors and versions of
Python:

* :doc:`Jython support <howto/jython>`
* :doc:`Python 3 compatibility <topics/python3>`


The Django open-source project
==============================

Learn about the development process for the Django project itself and about how
you can contribute:

* **Community:**
  :doc:`How to get involved <internals/contributing/index>` |
  :doc:`The release process <internals/release-process>` |
  :doc:`Team organization <internals/organization>` |
  :doc:`Meet the team <internals/team>` |
  :doc:`Current roles <internals/roles>` |
  :doc:`The Django source code repository <internals/git>`

* **Third-party distributions:**
  :doc:`Overview <misc/distributions>`

* **Django over time:**
  :doc:`API stability <misc/api-stability>` |
  :doc:`Release notes and upgrading instructions <releases/index>` |
  :doc:`Deprecation Timeline <internals/deprecation>`