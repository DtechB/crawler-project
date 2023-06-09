import Analyzer
import sys

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.utils import timezone

from .models import Subdomain, SecureSocketsLayersCertificate, Site, Link
from .serializer import SubdomainSerializer, SecureSocketsLayersCertificateSerializer, SiteSerializer, LinkSerializer

sys.path.append("..")


@api_view(['GET', 'POST'])
def getSubdomains(request):
    if request.method == 'GET':
        site_id = request.GET.get('site')
        if site_id:
            try:
                subdomains = Subdomain.objects.filter(site=site_id)
            except Subdomain.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            subdomains = Subdomain.objects.all()
        serializer = SubdomainSerializer(subdomains, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = Subdomain.objects.filter(base='sharoodut.ac.ir').values()
        serializer = SubdomainSerializer(data, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def getSecureSocketsLayersCertificate(request):
    if request.method == 'GET':
        site_id = request.GET.get('site')
        if site_id:
            try:
                secureSocketsLayersCertificate = SecureSocketsLayersCertificate.objects.filter(
                    site=site_id)
            except SecureSocketsLayersCertificate.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            secureSocketsLayersCertificate = SecureSocketsLayersCertificate.objects.all()
        serializer = SecureSocketsLayersCertificateSerializer(
            secureSocketsLayersCertificate, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print(request.data['url'])
        data = SecureSocketsLayersCertificate.objects.filter(
            url=request.data['url']).values()
        serializer = SecureSocketsLayersCertificateSerializer(data, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def runAnalyzer(request):
    if request.method == 'GET':
        Analyzer.analyze()
        return Response("Analyze Finished")


class SiteViewSet(viewsets.ModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__id']


@api_view(['GET'])
def getLinks(request):
    if request.method == 'GET':
        site_id = request.GET.get('site')
        if site_id:
            try:
                link = Link.objects.filter(site=site_id)
            except Link.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            link = Link.objects.all()
        serializer = LinkSerializer(link, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getStatistics(request):
    if request.method == 'GET':
        today = datetime.now()
        last_week = today - timezone.timedelta(days=7)
        link_count_by_day = Link.objects.filter(created_at__gte=last_week) \
            .extra({'day': 'date(created_at)'}) \
            .values('day') \
            .annotate(count=Count('id')).order_by('day')

        sites_count_by_day = Site.objects.filter(created_at__gte=last_week) \
            .extra({'day': 'date(created_at)'}) \
            .values('day') \
            .annotate(count=Count('id')).order_by('day')

        subdomain_count_by_day = Subdomain.objects.filter(created_at__gte=last_week) \
            .extra({'day': 'date(created_at)'}) \
            .values('day') \
            .annotate(count=Count('id')).order_by('day')

        # Calculate the start date and end date for last week
        last_week_start = today - timedelta(days=6)
        last_week_end = today

        # Create an empty list to store the dates
        dates_last_week = []
        link_counts = []
        site_counts = []
        sub_counts = []

        # Loop through each day of the last week and append it to the list
        current_date = last_week_start
        while current_date <= last_week_end:
            dates_last_week.append(current_date.date())
            current_date += timedelta(days=1)

        for d in dates_last_week:
            count = 0
            count1 = 0
            count2 = 0
            for link_count in link_count_by_day:
                if link_count['day'] == d:
                    count = link_count['count']

            for site_count in sites_count_by_day:
                if site_count['day'] == d:
                    count1 = site_count['count']

            for sub_count in subdomain_count_by_day:
                if sub_count['day'] == d:
                    count2 = sub_count['count']

            link_counts.append(count)
            site_counts.append(count1)
            sub_counts.append(count2)

        return Response({"links": link_counts, "sites": site_counts, "subs": sub_counts})
