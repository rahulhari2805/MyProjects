# Generated by Django 3.0.8 on 2020-08-15 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20200815_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction_Winner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winner', models.CharField(max_length=64)),
                ('Auction_user', models.CharField(max_length=64)),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('url_image', models.CharField(max_length=255)),
                ('price_bid', models.IntegerField()),
                ('winner_bid', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='auction_listing',
            name='auction_winner',
        ),
    ]