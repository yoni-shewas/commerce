# Generated by Django 5.0.3 on 2024-03-31 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='datListed',
            field=models.DateTimeField(auto_now_add=True, default='2024-04-01 08:00'),
            preserve_default=False,
        ),
    ]