import os

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .models import Subdomain, SecureSocketsLayersCertificate, Site
from .serializer import SubdomainSerializer, SecureSocketsLayersCertificateSerializer, SiteSerializer

@api_view(['GET', 'POST'])
def getSubdomains(request):
    if request.method == 'GET':
        subdomain = Subdomain.objects.all()
        serializer = SubdomainSerializer(subdomain, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = Subdomain.objects.filter(base='sharoodut.ac.ir').values()
        serializer = SubdomainSerializer(data, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def getSecureSocketsLayersCertificate(request):
    if request.method == 'GET':
        secureSocketsLayersCertificate = SecureSocketsLayersCertificate.objects.all()
        serializer = SecureSocketsLayersCertificateSerializer(
            secureSocketsLayersCertificate, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data['url'])
        data = SecureSocketsLayersCertificate.objects.filter(url=request.data['url']).values()
        serializer = SecureSocketsLayersCertificateSerializer(data, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def runAnalyzer(request):
    if request.method == 'GET':
        os.system("python C:/Users/MosKn/Desktop/crawler-project/Analyzer.py")
        return Response("Analyze Finished")


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__id']
