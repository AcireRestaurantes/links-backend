# Generated by Django 4.2.1 on 2024-09-19 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0002_remove_userprofile_image_url_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default='Seu Nome Profissional', max_length=100),
        ),
    ]