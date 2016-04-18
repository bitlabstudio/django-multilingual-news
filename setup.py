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
        'Django>=1.8.1',
        'django-hvad>=1.5',
        'django-filer>=1.0.0',
        'Pillow>=2.4.0',
        'django-document-library',
        'django-people>=1.1',
        'django-multilingual-tags',
        'django-cms>=3.0',
    ],
)
