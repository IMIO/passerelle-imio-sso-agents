# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-30 12:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0013_delete_templatevar'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImioSsoAgents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('slug', models.SlugField(unique=True, verbose_name='Identifier')),
                ('csv_file', models.FileField(help_text='Supported file formats: csv', upload_to=b'agents_csv', verbose_name='Agents csv file')),
                ('ignore_types', models.CharField(blank=True, default=b'', max_length=128, verbose_name='Types to ignore')),
                ('users', models.ManyToManyField(blank=True, related_name='_imiossoagents_users_+', related_query_name='+', to='base.ApiUser')),
            ],
            options={
                'verbose_name': "imio.memory CSV to JSON that be comsumme by WCA.",
            },
        ),
    ]
