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
    status = models.CharField(
        max_length=1, choices=STATUS, default=STATUS_PENDING)
    user = models.ManyToManyField(User, related_name='site', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # I Think it's better to show full string for this section

    def __str__(self):
        if self.status == 'P':
            return f"Pending -- {self.url}"
        else:
            return f"Active -- {self.url}"


class Subdomain(models.Model):
    base = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=511)
    ip = models.CharField(max_length=63)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.base} : {self.subdomain}"


class SecureSocketsLayersCertificate(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length=511, null=True)
    issuedto = models.CharField(max_length=63, null=True)
    issuedby = models.CharField(max_length=63, null=True)
    validfrom = models.CharField(max_length=63, null=True)
    validto = models.CharField(max_length=63, null=True)
    validdays = models.CharField(max_length=63, null=True)
    certivalid = models.CharField(max_length=63, null=True)
    certisn = models.CharField(max_length=63, null=True)
    certiver = models.CharField(max_length=63, null=True)
    certialgo = models.CharField(max_length=63, null=True)
    expired = models.CharField(max_length=63, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.site}"


class Crawler(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length=31)
    broken_link = models.CharField(max_length=2047)


class Link(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length=255)
    status_code = models.IntegerField(default=200)
    created_at = models.DateTimeField(auto_now_add=True)
