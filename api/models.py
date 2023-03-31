from django.db import models


class Subdomain(models.Model):
    base = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=511)
    ip = models.CharField(max_length=63)


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
