# Generated by Django 5.0.1 on 2024-04-02 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videoDownloader', '0004_alter_downloaded_author_alter_downloaded_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='downloaded',
            name='res',
            field=models.CharField(choices=[('highest', 'Highest Resolution'), ('720p', '720p'), ('480p', '480p'), ('360p', '360p'), ('lowest', 'Lowest Resolution')], max_length=10),
        ),
    ]
