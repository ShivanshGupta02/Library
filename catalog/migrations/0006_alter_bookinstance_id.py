# Generated by Django 4.1.1 on 2023-04-04 14:24

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique id for this particular book across the whole library', primary_key=True, serialize=False),
        ),
    ]
