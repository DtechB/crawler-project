# Generated by Django 4.1.3 on 2023-03-31 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ssl',
            new_name='SecureSocketsLayersCertificate',
        ),
    ]
