# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 07:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Abacus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.TextField(default='', max_length=255)),
                ('descriable', models.TextField(default='', max_length=255)),
                ('create_date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('shared', models.BooleanField(default=False)),
                ('status', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='abacus', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-create_date',),
            },
        ),
    ]
