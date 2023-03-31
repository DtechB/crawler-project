from rest_framework import serializers
from .models import Subdomain, SecureSocketsLayersCertificate


class SubdomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subdomain
        fields = ('base', 'subdomain', 'ip')


class SecureSocketsLayersCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureSocketsLayersCertificate
        fields = ('url', 'issuedto', 'issuedby', 'validfrom', 'validto',
                  'validdays', 'certivalid', 'certisn', 'certiver', 'certialgo', 'expired')
