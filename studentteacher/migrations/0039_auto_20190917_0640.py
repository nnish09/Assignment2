# Generated by Django 2.2.5 on 2019-09-17 06:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('studentteacher', '0038_auto_20190917_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='uploaded_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 6, 40, 39, 395708)),
        ),
        migrations.AlterField(
            model_name='chat',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2019, 9, 17, 6, 40, 39, 397675, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='submission',
            name='submitted_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 9, 17, 6, 40, 39, 396377)),
        ),
    ]