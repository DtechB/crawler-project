from rest_framework import serializers
from .models import Subdomain, SecureSocketsLayersCertificate, Site, Link


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


class SubdomainSerializer(serializers.ModelSerializer):
    site = SiteSerializer()

    class Meta:
        model = Subdomain
        fields = ('base', 'subdomain', 'ip', 'site')


class SecureSocketsLayersCertificateSerializer(serializers.ModelSerializer):
    site = SiteSerializer()

    class Meta:
        model = SecureSocketsLayersCertificate
        fields = ('url', 'issuedto', 'issuedby', 'validfrom', 'validto',
                  'validdays', 'certivalid', 'certisn', 'certiver', 'certialgo', 'expired', 'site')
        

class LinkSerializer(serializers.ModelSerializer):
    site = SiteSerializer()

    class Meta:
        model = Link
        fields = ('url', 'status_code', 'site')
