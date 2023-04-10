from django.contrib import admin
from .models import Subdomain, Site, SecureSocketsLayersCertificate, urlsUnchecked, urlsChecked

admin.site.register(Subdomain)
admin.site.register(SecureSocketsLayersCertificate)
admin.site.register(urlsUnchecked)
admin.site.register(urlsChecked)
admin.site.register(Site)
