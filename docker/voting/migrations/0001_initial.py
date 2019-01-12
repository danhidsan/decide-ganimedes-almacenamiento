# Generated by Django 2.0.8 on 2019-01-11 11:58

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(editable=False, null=True)),
                ('desc', models.TextField()),
                ('help_text', models.TextField(blank=True, max_length=300, null=True)),
                ('yes_no_question', models.BooleanField(default=False, help_text='Check the box to generate automatically the options yes/no ', verbose_name='Yes/No question')),
                ('seats', models.PositiveIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(editable=False, null=True)),
                ('option', models.TextField()),
                ('weight', models.IntegerField(blank=True, null=True)),
                ('gender', models.NullBooleanField(choices=[(True, 'Male'), (False, 'Female')])),
                ('team', models.IntegerField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='voting.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('desc', models.TextField(blank=True, null=True)),
                ('postproc_type', models.IntegerField(blank=True, choices=[(0, 'Identity'), (1, 'Weight'), (2, 'Seats'), (3, 'Parity'), (4, 'Team')], default=0, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('tally', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('postproc', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('auths', models.ManyToManyField(related_name='votings', to='base.Auth')),
                ('pub_key', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='voting', to='base.Key')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='voting',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='voting.Voting'),
        ),
    ]