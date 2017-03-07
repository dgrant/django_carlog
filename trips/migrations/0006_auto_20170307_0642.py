# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_remove_car_license_plate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='name',
            field=models.CharField(unique=True, max_length=20),
        ),
    ]
