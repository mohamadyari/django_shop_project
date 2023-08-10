# Generated by Django 3.2.6 on 2021-09-28 21:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0006_remove_variants_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_view',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='view',
            field=models.ManyToManyField(blank=True, null=True, related_name='product_view', to=settings.AUTH_USER_MODEL),
        ),
    ]
