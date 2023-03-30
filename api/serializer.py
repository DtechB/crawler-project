from rest_framework import serializers
from .models import Subdomain, Ssl


class SubdomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subdomain
        fields = ('base', 'subdomain', 'ip')


class SslSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ssl
        fields = ('url', 'issuedto', 'issuedby', 'validfrom', 'validto',
                  'validdays', 'certivalid', 'certisn', 'certiver', 'certialgo', 'expired')
