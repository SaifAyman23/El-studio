# Generated by Django 5.0.1 on 2024-04-02 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoDownloader', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='downloaded',
            name='res',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='downloaded',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
