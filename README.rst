Django Multilingual News
========================

A reusable Django app for managing news/blog entries in different languages.

Comes with a django-cms apphook and has been prepared using Django 1.5.1 and
django-cms 2.4.1. From version 2.0 onwards it is tested and developed further
on Django 1.9 and django-cms 3.

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
        'django_libs',
        'multilingual_news',
        'people',
        'hvad',
        'multilingual_tags',
        'document_library',

        # cms related requirements (please check the relevant `documentation <https://github.com/divio/django-cms>`)
        'cms',
        'menus',
        'treebeard',
        
        # filer related requirements (please check the relevant `documentation <https://github.com/divio/django-filer>`)
        'filer',
        'easy_thumbnails',
    )

Run the migrations::

    ./manage.py migrate


Usage
-----

Placeholders ("excerpt" and "content")
++++++++++++++++++++++++++++++++++++++

To add content to a news entry, you can make use of two cms placeholders. The excerpt is used in list views only. Adding content to a placeholder works pretty much the same like adding content to a cms page. First, create a news entry, then go to its detail view. Use the django cms toolbar to add plugins to the placeholders. For more information visit `Django CMS' documentation <http://docs.django-cms.org/en/latest/introduction/templates_placeholders.html#placeholders>`_.

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

    {% load multilingual_news_tags %}
    {% get_recent_news limit=5 as recent_news %}
    {% include "multilingual_news/recent.html" with object_list=recent_news %}

You might want to filter recent news by a category. Just add the relevant
category slug::

    {% get_recent_news category='category-slug' as recent_news %}

If you want to render recent news on a news detail page, you might want to
exclude the current news from the queryset::

    {% get_recent_news exclude=object as recent_news %}


get_newsentry_meta_description and get_newsentry_meta_title
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

To render the best matching title or description from the SEO fields, you can
use the template tags ``get_newsentry_meta_description`` and
``get_newsentry_meta_title``. ::

    <title>{% get_newsentry_meta_title entry_instance %}</title>
    <meta name="description" content="{% get_newsentry_meta_description entry_instance %}" />
    
    
Twitter Bootstrap 3
-------------------

List of Bootstrap compatible features:

* A delete confirmation modal for deleting news entries.

For support of the Twitter Bootstrap 3 functionality, you need to add the Bootstrap js library to your template. If you haven't already 

.. code-block:: html


    <script type="text/javascript" src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>


Delete confirmation modal
+++++++++++++++++++++++++

Add the following markup to your template.

.. code-block:: html

    {% load static %}

    {# add this before bootstrap.js #}
    <script type="text/javascript" src="{% static "django_libs/js/modals.js" %}"></script>

    <div id="ajax-modal" class="modal fade" tabindex="-1">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>
            </div>
            <div class="modal-body">
            </div>
        </div>
    </div>

To trigger the modal, create a link that looks like this.

.. code-block:: html

    <a href="{% url "news_delete" pk=news_entry.pk %}" data-class="toggleDeleteModal">Delete</a>


Settings
--------

NEWS_PAGINATION_AMOUNT
++++++++++++++++++++++

Default: 10

Amount of news entries to display in the list view.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-multilingual-news
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch

In order to run the tests, simply execute ``tox``. This will install two new
environments (for Django 1.8 and Django 1.9) and run the tests against both
environments.
