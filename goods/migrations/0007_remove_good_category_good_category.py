# Generated by Django 5.0.2 on 2024-02-19 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0006_category_good_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='good',
            name='category',
        ),
        migrations.AddField(
            model_name='good',
            name='category',
            field=models.ManyToManyField(to='goods.category'),
        ),
    ]