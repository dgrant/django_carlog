# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0004_auto_20150207_0447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='license_plate',
        ),
    ]
