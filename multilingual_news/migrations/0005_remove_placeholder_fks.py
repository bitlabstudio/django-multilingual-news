from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("multilingual_news", "0004_placeholder_relation"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="newsentry",
            name="excerpt",
        ),
        migrations.RemoveField(
            model_name="newsentry",
            name="content",
        ),
    ]
