from django.db import models
from django.contrib.auth.models import User


class Site(models.Model):
    STATUS_PENDING = 'P'
    STATUS_ACTIVE = 'A'
    STATUS = [
        ('P', 'pending'),
        ('A', 'active')
    ]
    url = models.CharField(max_length=1024)
    status = models.CharField(max_length=1, choices=STATUS, default=STATUS_PENDING)
    user = models.ManyToManyField(User, related_name='site', blank=True)

    def __str__(self):
        return f"{self.status} -- {self.url}"


class Subdomain(models.Model):
    base = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=511)
    ip = models.CharField(max_length=63)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)


class SecureSocketsLayersCertificate(models.Model):
    url = models.CharField(max_length=511)
    issuedto = models.CharField(max_length=63)
    issuedby = models.CharField(max_length=63)
    validfrom = models.CharField(max_length=63)
    validto = models.CharField(max_length=63)
    validdays = models.CharField(max_length=63)
    certivalid = models.CharField(max_length=63)
    certisn = models.CharField(max_length=63)
    certiver = models.CharField(max_length=63)
    certialgo = models.CharField(max_length=63)
    expired = models.CharField(max_length=63)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)


class urlsUnchecked(models.Model):
    userID = models.CharField(max_length=31)
    url = models.CharField(max_length=127)


class urlsChecked(models.Model):
    userID = models.CharField(max_length=31)
    url = models.CharField(max_length=127)


class BrokenUrls(models.Model):
    site_url = models.CharField(max_length=31)
    broken_link = models.CharField(max_length=127)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)


class UrlChecked(models.Model):
    url = models.CharField(max_length=31)
    hits = models.IntegerField()
    broken_links_num = models.IntegerField()
