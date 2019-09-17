# Generated by Django 2.2.5 on 2019-09-09 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentteacher', '0005_auto_20190909_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'student'), (2, 'teacher')], default='student'),
        ),
    ]
