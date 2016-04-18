# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import cms.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_urlconfrevision'),
        ('people', '__first__'),
        ('filer', '0002_auto_20150606_2003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(max_length=512, verbose_name='Slug')),
                ('hide_on_list', models.BooleanField(default=False, verbose_name='Hide on list view')),
                ('parent', models.ForeignKey(verbose_name='Parent', blank=True, to='multilingual_news.Category', null=True)),
            ],
            options={
                'ordering': ('slug',),
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='CategoryPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('template_argument', models.CharField(max_length=20, verbose_name='Template Argument', blank=True)),
                ('categories', models.ManyToManyField(to='multilingual_news.Category', verbose_name='Category')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='CategoryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256, verbose_name='Title')),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='multilingual_news.Category', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'multilingual_news_category_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='NewsEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateTimeField(null=True, verbose_name='Publication date', blank=True)),
                ('image_float', models.CharField(blank=True, max_length=8, verbose_name='Image float', choices=[(b'left', 'Left'), (b'right', 'Right')])),
                ('image_width', models.IntegerField(null=True, verbose_name='Image width', blank=True)),
                ('image_height', models.IntegerField(null=True, verbose_name='Image height', blank=True)),
                ('image_source_url', models.CharField(max_length=1024, verbose_name='Image source URL', blank=True)),
                ('image_source_text', models.CharField(max_length=1024, verbose_name='Image source text', blank=True)),
                ('author', models.ForeignKey(verbose_name='Author', blank=True, to='people.Person', null=True)),
                ('categories', models.ManyToManyField(related_name='newsentries', verbose_name='Categories', to='multilingual_news.Category')),
                ('content', cms.models.fields.PlaceholderField(related_name='multilingual_news_contents', slotname='multilingual_news_content', blank=True, editable=False, to='cms.Placeholder', null=True)),
                ('excerpt', cms.models.fields.PlaceholderField(related_name='multilingual_news_excerpts', slotname='multilingual_news_excerpt', blank=True, editable=False, to='cms.Placeholder', null=True)),
                ('image', filer.fields.image.FilerImageField(verbose_name='Image', blank=True, to='filer.Image', null=True)),
                ('thumbnail', filer.fields.image.FilerImageField(related_name='entries_with_thumbnails', verbose_name='Thumbnail', blank=True, to='filer.Image', null=True)),
            ],
            options={
                'ordering': ('-pub_date',),
                'verbose_name': 'News Entry',
                'verbose_name_plural': 'News Entries',
            },
        ),
        migrations.CreateModel(
            name='NewsEntryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=512, verbose_name='Title')),
                ('slug', models.SlugField(max_length=512, verbose_name='Slug')),
                ('is_published', models.BooleanField(default=False, verbose_name='Is published')),
                ('meta_title', models.CharField(help_text='Best to keep this below 70 characters', max_length=128, null=True, verbose_name='Meta title', blank=True)),
                ('meta_description', models.TextField(help_text='Best to keep this below 160 characters', max_length=512, null=True, verbose_name='Meta description', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='multilingual_news.NewsEntry', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'multilingual_news_newsentry_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.AlterUniqueTogether(
            name='newsentrytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='categorytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
