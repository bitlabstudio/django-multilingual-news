from django.db import migrations


def migrate_placeholders_forward(apps, schema_editor):
    """
    Migrate PlaceholderField FKs to GenericForeignKey-based PlaceholderRelationField.

    For each NewsEntry, update the linked Placeholder objects (excerpt, content)
    to set content_type and object_id so that PlaceholderRelationField can find them.
    """
    NewsEntry = apps.get_model("multilingual_news", "NewsEntry")
    ContentType = apps.get_model("contenttypes", "ContentType")
    ct = ContentType.objects.get_for_model(NewsEntry)

    for entry in NewsEntry.objects.filter(excerpt__isnull=False):
        entry.excerpt.content_type = ct
        entry.excerpt.object_id = entry.pk
        entry.excerpt.save(update_fields=["content_type", "object_id"])

    for entry in NewsEntry.objects.filter(content__isnull=False):
        entry.content.content_type = ct
        entry.content.object_id = entry.pk
        entry.content.save(update_fields=["content_type", "object_id"])


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("cms", "0041_alter_pageurl_unique_together_pageurl_site_and_more"),
        ("multilingual_news", "0003_auto_20220505_0002"),
    ]

    operations = [
        migrations.RunPython(
            migrate_placeholders_forward,
            migrations.RunPython.noop,
        ),
    ]
