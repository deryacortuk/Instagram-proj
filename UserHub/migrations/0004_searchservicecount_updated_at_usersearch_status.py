# Generated by Django 4.2.5 on 2023-10-28 19:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("UserHub", "0003_searchservicecount"),
    ]

    operations = [
        migrations.AddField(
            model_name="searchservicecount",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="usersearch",
            name="status",
            field=models.BooleanField(default=False),
        ),
    ]
