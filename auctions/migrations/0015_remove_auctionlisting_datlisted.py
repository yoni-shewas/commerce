# Generated by Django 5.0.3 on 2024-03-31 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_auctionlisting_datlisted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='datListed',
        ),
    ]