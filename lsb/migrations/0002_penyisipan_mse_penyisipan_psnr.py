# Generated by Django 4.2.9 on 2024-06-18 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lsb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='penyisipan',
            name='mse',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='penyisipan',
            name='psnr',
            field=models.FloatField(null=True),
        ),
    ]
