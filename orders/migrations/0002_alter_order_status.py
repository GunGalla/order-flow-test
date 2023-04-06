# Generated by Django 4.2 on 2023-04-06 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'new'), ('accepted', 'accepted'), ('failed', 'failed')], default='new', max_length=12),
        ),
    ]
