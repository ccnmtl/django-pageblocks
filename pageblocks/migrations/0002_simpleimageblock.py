# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pageblocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleImageBlock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'images')),
                ('caption', models.TextField(blank=True)),
                ('alt', models.CharField(max_length=100, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
