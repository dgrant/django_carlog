# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_odometer_km'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='distance',
            field=models.DecimalField(max_digits=5, decimal_places=1),
            preserve_default=True,
        ),
    ]
