# Generated by Django 4.1.5 on 2023-02-02 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_alter_user_gender_alter_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_signed',
            field=models.BooleanField(default=False),
        ),
    ]
