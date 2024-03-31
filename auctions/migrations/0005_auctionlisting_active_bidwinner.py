# Generated by Django 5.0.3 on 2024-03-30 16:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_watchlisting'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='bidWinner',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('winning_bid', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_won', models.DateTimeField(auto_now_add=True)),
                ('bidWinner', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bidWinner', to=settings.AUTH_USER_MODEL)),
                ('bidWon', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bidWinner', to='auctions.auctionlisting')),
            ],
        ),
    ]