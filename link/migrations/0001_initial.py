# Generated by Django 2.2.3 on 2019-09-24 10:40

from django.db import migrations, models
import link.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UPILink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.TextField()),
                ('identifier', models.CharField(default=link.models.get_random_string, max_length=20)),
            ],
        ),
    ]
