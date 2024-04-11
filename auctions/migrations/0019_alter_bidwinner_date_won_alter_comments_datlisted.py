# Generated by Django 5.0.3 on 2024-04-11 06:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auctionlisting_datlisted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidwinner',
            name='date_won',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='comments',
            name='datListed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]