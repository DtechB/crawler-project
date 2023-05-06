from django.contrib import admin
from .models import Subdomain, Site, SecureSocketsLayersCertificate, Link

admin.site.register(Subdomain)
admin.site.register(SecureSocketsLayersCertificate)
admin.site.register(Site)
admin.site.register(Link)