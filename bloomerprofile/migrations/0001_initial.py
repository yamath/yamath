# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-02 22:48
from __future__ import unicode_literals

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=4, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassroomBloomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Envelope',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, null=True)),
                ('option', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='envelope_option', to='content.Option')),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='envelope_question', to='content.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Mean',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.CharField(default='XXXXXXXXXX', max_length=10)),
                ('forget', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SerieClassroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serieclassroom_classroom', to='bloomerprofile.Classroom')),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='serieclassroom_serie', to='content.Serie')),
            ],
        ),
        migrations.CreateModel(
            name='Bloomer',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='mean',
            name='bloomer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mean_bloomer', to='bloomerprofile.Bloomer'),
        ),
        migrations.AddField(
            model_name='mean',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mean_topic', to='content.Topic'),
        ),
        migrations.AddField(
            model_name='envelope',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='envelope_receiver', to='bloomerprofile.Bloomer'),
        ),
        migrations.AddField(
            model_name='envelope',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='envelope_sender', to='bloomerprofile.Bloomer'),
        ),
        migrations.AddField(
            model_name='envelope',
            name='serie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='envelope_serie', to='content.Serie'),
        ),
        migrations.AddField(
            model_name='envelope',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='envelope_topic', to='content.Topic'),
        ),
        migrations.AddField(
            model_name='classroombloomer',
            name='bloomer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classroombloomer_bloomer', to='bloomerprofile.Bloomer'),
        ),
        migrations.AddField(
            model_name='classroombloomer',
            name='classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classroombloomer_classroom', to='bloomerprofile.Classroom'),
        ),
    ]
