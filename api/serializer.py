from rest_framework import serializers
from .models import Subdomain, SecureSocketsLayersCertificate, urlsUnchecked, urlsChecked, Site


class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


class SubdomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subdomain
        fields = ('base', 'subdomain', 'ip')


class SecureSocketsLayersCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecureSocketsLayersCertificate
        fields = ('url', 'issuedto', 'issuedby', 'validfrom', 'validto',
                  'validdays', 'certivalid', 'certisn', 'certiver', 'certialgo', 'expired')


class urlsUncheckedSerializer(serializers.ModelSerializer):
    class Meta:
        model = urlsUnchecked
        fields = ('userID', 'url')


class urlsCheckedSerializer(serializers.ModelSerializer):
    class Meta:
        model = urlsChecked
        fields = ('userID', 'url')