import os
from setuptools import setup, find_packages
import multilingual_news
try:
    import multiprocessing  # NOQA
except ImportError:
    pass


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''


setup(
    name="django-multilingual-news",
    version=multilingual_news.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.rst'),
    license='The MIT License',
    platforms=['OS Independent'],
    keywords='django, news, blog, multilingual, cms',
    author='Tobias Lorenz',
    author_email='tobias.lorenz@bitmazk.com',
    url="https://github.com/bitmazk/django-multilingual-news",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.6.2',
        'django-hvad>=0.4',
        'djangocms-utils>=0.9.5',
        'django-filer>=0.9.4',
        'Pillow>=2.4.0',
        'South',
        'django-document-library',
        'django-people',
        'django-multilingual-tags',
        'django-cms>=3.0',
    ],
    tests_require=[
        'fabric',
        'factory_boy>=2.0.0',
        'django-libs>=1.45',
        'django-nose',
        'coverage',
        'django-coverage',
        'mock',
        'djangocms-text-ckeditor',
        'djangocms-link',
    ],
    test_suite='multilingual_news.tests.runtests.runtests',
)
