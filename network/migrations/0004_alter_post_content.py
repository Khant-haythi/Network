# Generated by Django 4.2.16 on 2024-12-03 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(),
        ),
    ]
