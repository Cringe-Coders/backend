# Generated by Django 4.2.6 on 2023-10-20 17:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0003_alter_event_participant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='participant',
            field=models.ManyToManyField(related_name='events', to=settings.AUTH_USER_MODEL),
        ),
    ]
