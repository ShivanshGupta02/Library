# Generated by Django 4.1.1 on 2023-01-12 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermembership',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'pending'), ('PAID', 'paid')], default='pending', max_length=100),
        ),
    ]
