Django Multilingual News
========================

A reusable Django app for managing news/blog entries in different languages.

Comes with a django-cms apphook and has been prepared using Django 1.5.1 and
django-cms 2.4.1.

This app is based on the great https://github.com/fivethreeo/cmsplugin-bloghttps://github.com/fivethreeo/cmsplugin-blog
and re-used some of it's snippets.


Installation
------------

If you want to install the latest stable release from PyPi::

    $ pip install django-multilingual-news

If you feel adventurous and want to install the latest commit from GitHub::

    $ pip install -e git://github.com/bitmazk/django-multilingual-news.git#egg=multilingual_news

Add ``multilingual_news`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...,
        'multilingual_news',
    )

Run the South migrations::

    ./manage.py migrate multilingual_news


Usage
-----

Using the apphook
+++++++++++++++++

Simply create a django-cms page and select it in the ``Application`` field of
the ``Advanced Settings``.

Template tags
+++++++++++++

We provide a template tag to render the news entry's placeholder. First import
the tag library, then add the tag plus arguments::

    {% load multilingual_news_tags %}
    {% render_news_placeholder NEWS_ENTRY_OBJECT OPTIONAL_PLACEHOLDER_SLOT OPTIONAL_TRUNCATION %}

To render the first non-empty placeholder (e.g. if the excerpt is empty)::

    {% render_news_placeholder news_entry %}

To render the ``excerpt``::

    {% render_news_placeholder news_entry 'excerpt' %}

To render the ``content``::

    {% render_news_placeholder news_entry 'content' %}

To render and truncate the ``content`` (10 words)::

    {% render_news_placeholder news_entry 'content' 10 %}

To render and truncate the first non-empty placeholder (20 words)::

    {% render_news_placeholder news_entry 20 %}


Settings
--------

NEWS_PAGINATION_AMOUNT
++++++++++++++++++++++

Default: 10

Amount of news entries to display in the list view.


Contribute
----------

If you want to contribute to this project, please perform the following steps::

    # Fork this repository
    # Clone your fork
    $ mkvirtualenv -p python2.7 django-multilingual-news
    $ pip install -r requirements.txt
    $ ./logger/tests/runtests.sh
    # You should get no failing tests

    $ git co -b feature_branch master
    # Implement your feature and tests
    # Describe your change in the CHANGELOG.txt
    $ git add . && git commit
    $ git push origin feature_branch
    # Send us a pull request for your feature branch

Whenever you run the tests a coverage output will be generated in
``tests/coverage/index.html``. When adding new features, please make sure that
you keep the coverage at 100%.


Roadmap
-------

Check the issue tracker on github for milestones and features to come.
