# Generated by Django 4.1.5 on 2023-01-12 09:22

import datetime
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
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('index', models.TextField(max_length=255)),
                ('youtube_link', models.TextField()),
                ('parent_id', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2023, 1, 12, 18, 22, 39, 546536), null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
