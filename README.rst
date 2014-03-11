Django Multilingual News
========================

A reusable Django app for managing news/blog entries in different languages.

Comes with a django-cms apphook and has been prepared using Django 1.5.1 and
django-cms 2.4.1. From version 2.0 onwards it is tested and developed further
on Django 1.6.2 and django-cms 3.

This app is based on the great https://github.com/fivethreeo/cmsplugin-blog
and re-used some of it's snippets.

Current features include

- Entry authors based on a `django-people <http://github.com/bitmazk/django-people/>`_ Person
- Entry attachments based on the `django-document-library <http://github.com/bitmazk/django-document-library>`_ Document
- Tagging via `django-multilingual-tags <http://github.com/bitmazk/django-multilingual-tags>`_ with a tag based archive view
- Entry categories
- RSS Feeds for all news entries, just special authors or tag based.
- Site maps
- SEO fields on the Entry for storing custom individual meta descriptions and
  titles.


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

Simply create a django-cms page and select ``Multilingual News Apphook`` in the
``Application`` field of the ``Advanced Settings``.


Sitemaps
++++++++

To add a sitemap of your blog, add the following to your urlconf: ::

    from multilingual_news.sitemaps import NewsSitemap

    urlpatterns += patterns(
        '',
        url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {
            'sitemaps': {
                'blogentries': NewsSitemap,
            }, }),
    )

RSS Feeds
+++++++++

The app provides three different types of feeds, you can link to.

1. All news ``{% url "news_rss" %}``
2. News from a specific author ``{% url "news_rss_author" author=author.pk %}``,
   where ``author`` is an instance of a ``people.Person``
3. All news ``{% url "news_rss_tagged" tag=tag.slug %}``, where ``Tag`` is an
   instance of a ``multilingual_tags.Tag``.


Tagging
+++++++

You can simply add tags for a news entry from the ``NewsEntry`` admin page,
which renders an inline form at the bottom.


Template tags
-------------

get_recent_news
+++++++++++++++

To render recent news::

    {% get_recent_news limit=5 as recent_news %}
    {% include "multilingual_news/recent.html" with object_list=recent_news %}

If you want to render recent news on a news detail page, you might want to
exclude the current news from the queryset::

    {% get_recent_news exclude=object as recent_news %}
    {% include "multilingual_news/recent.html" with object_list=recent_news %}


get_newsentry_meta_description and get_newsentry_meta_title
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

To render the best matching title or description from the SEO fields, you can
use the template tags ``get_newsentry_meta_description`` and
``get_newsentry_meta_title``. ::

    <title>{% get_newsentry_meta_title entry_instance %}</title>
    <meta name="description" content="{% get_newsentry_meta_description entry_instance %}" />


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
