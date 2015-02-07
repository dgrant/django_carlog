# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0002_auto_20150207_0440'),
    ]

    operations = [
        migrations.AddField(
            model_name='odometer',
            name='km',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
