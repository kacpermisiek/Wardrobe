# Generated by Django 4.1.2 on 2022-11-13 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0002_delete_currentsettemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
