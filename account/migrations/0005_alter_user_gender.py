# Generated by Django 4.1.5 on 2023-01-15 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.TextField(max_length=1, null=True),
        ),
    ]