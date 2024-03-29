# Generated by Django 2.2.28 on 2022-05-05 05:02

from django.db import migrations, models
import django.db.models.deletion
import parler.fields


class Migration(migrations.Migration):

    dependencies = [
        ('multilingual_news', '0002_recentplugin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorytranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'Category Translation'},
        ),
        migrations.AlterModelOptions(
            name='newsentrytranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'News Entry Translation'},
        ),
        migrations.AlterField(
            model_name='categoryplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='multilingual_news_categoryplugin', serialize=False, to='cms.CMSPlugin'),
        ),
        migrations.AlterField(
            model_name='categorytranslation',
            name='language_code',
            field=models.CharField(db_index=True, max_length=15, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='categorytranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='multilingual_news.Category'),
        ),
        migrations.AlterField(
            model_name='newsentry',
            name='image_float',
            field=models.CharField(blank=True, choices=[('left', 'Left'), ('right', 'Right')], max_length=8, verbose_name='Image float'),
        ),
        migrations.AlterField(
            model_name='newsentrytranslation',
            name='language_code',
            field=models.CharField(db_index=True, max_length=15, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='newsentrytranslation',
            name='master',
            field=parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='multilingual_news.NewsEntry'),
        ),
        migrations.AlterField(
            model_name='recentplugin',
            name='cmsplugin_ptr',
            field=models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='multilingual_news_recentplugin', serialize=False, to='cms.CMSPlugin'),
        ),
    ]
