# Generated by Django 3.2.6 on 2021-09-28 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20210928_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='change',
            field=models.BooleanField(default=False),
        ),
    ]
