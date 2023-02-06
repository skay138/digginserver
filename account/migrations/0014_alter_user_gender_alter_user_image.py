# Generated by Django 4.1.5 on 2023-01-30 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.TextField(help_text='M or F', max_length=1, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(null=True, upload_to='profile_image/'),
        ),
    ]