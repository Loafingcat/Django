# Generated by Django 4.2.2 on 2023-07-02 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_head_image_alter_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='file_upload',
            field=models.FileField(blank=True, upload_to='blog/files/%Y/%m/%d/'),
        ),
    ]
