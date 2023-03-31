from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializer import SubdomainSerializer, SecureSocketsLayersCertificateSerializer
from .models import Subdomain, SecureSocketsLayersCertificate

@api_view(['GET'])
def getSubdomains(request):
    subdomain = Subdomain.objects.all()
    serializer = SubdomainSerializer(subdomain, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSecureSocketsLayersCertificate(request):
    secureSocketsLayersCertificate = SecureSocketsLayersCertificate.objects.all()
    serializer = SecureSocketsLayersCertificateSerializer(secureSocketsLayersCertificate, many=True)
    return Response(serializer.data)
