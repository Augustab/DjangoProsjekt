# Generated by Django 3.0.3 on 2020-12-09 18:01

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
            name='Account',
            fields=[
                ('name', models.CharField(default=None, max_length=50)),
                ('belop', models.IntegerField(default=0)),
                ('interest', models.CharField(default=None, max_length=50)),
                ('accountid', models.AutoField(db_column='accountid', primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Month',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Sum',
            fields=[
                ('sum', models.IntegerField(default=None)),
                ('beskrivelse', models.CharField(default=None, max_length=50)),
                ('date', models.DateField(blank=True, db_column='Sum_date', null=True, verbose_name='Sum_date')),
                ('month', models.IntegerField(default=None)),
                ('sumid', models.AutoField(db_column='sumid', primary_key=True, serialize=False)),
                ('account', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.Account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
