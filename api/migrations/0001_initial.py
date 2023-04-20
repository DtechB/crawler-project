# Generated by Django 4.1.3 on 2023-04-20 17:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=1024)),
                ('status', models.CharField(choices=[('P', 'pending'), ('A', 'active')], default='P', max_length=1)),
                ('user', models.ManyToManyField(blank=True, related_name='site', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subdomain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base', models.CharField(max_length=255)),
                ('subdomain', models.CharField(max_length=511)),
                ('ip', models.CharField(max_length=63)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.site')),
            ],
        ),
        migrations.CreateModel(
            name='SecureSocketsLayersCertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=511, null=True)),
                ('issuedto', models.CharField(max_length=63, null=True)),
                ('issuedby', models.CharField(max_length=63, null=True)),
                ('validfrom', models.CharField(max_length=63, null=True)),
                ('validto', models.CharField(max_length=63, null=True)),
                ('validdays', models.CharField(max_length=63, null=True)),
                ('certivalid', models.CharField(max_length=63, null=True)),
                ('certisn', models.CharField(max_length=63, null=True)),
                ('certiver', models.CharField(max_length=63, null=True)),
                ('certialgo', models.CharField(max_length=63, null=True)),
                ('expired', models.CharField(max_length=63, null=True)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.site')),
            ],
        ),
        migrations.CreateModel(
            name='BrokenUrls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_url', models.CharField(max_length=31)),
                ('broken_link', models.CharField(max_length=127)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.site')),
            ],
        ),
    ]
