from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import SubdomainSerializer, SslSerializer
from .models import Subdomain,Ssl

# Create your views here.
@api_view(['GET'])
def getSubdomains(request):
    subdomain = Subdomain.objects.all()
    serializer = SubdomainSerializer(subdomain, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSsls(request):
    ssl = Ssl.objects.all()
    serializer = SslSerializer(ssl, many=True)
    return Response(serializer.data)