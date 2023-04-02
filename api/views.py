from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import SubdomainSerializer, SecureSocketsLayersCertificateSerializer, urlsUncheckedSerializer, urlsCheckedSerializer
from .models import Subdomain, SecureSocketsLayersCertificate, urlsUnchecked, urlsChecked


@api_view(['GET'])
def getSubdomains(request):
    subdomain = Subdomain.objects.all()
    serializer = SubdomainSerializer(subdomain, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSecureSocketsLayersCertificate(request):
    secureSocketsLayersCertificate = SecureSocketsLayersCertificate.objects.all()
    serializer = SecureSocketsLayersCertificateSerializer(
        secureSocketsLayersCertificate, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def urlsUncheckedView(request):
    if request.method == 'GET':
        urlsUncheckedInstance = urlsUnchecked.objects.all()
        serializer = urlsUncheckedSerializer(urlsUncheckedInstance, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = urlsUncheckedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def geturlsChecked(request):
    urlsCheckedInstance = urlsChecked.objects.all()
    serializer = urlsCheckedSerializer(urlsCheckedInstance, many=True)
    return Response(serializer.data)
