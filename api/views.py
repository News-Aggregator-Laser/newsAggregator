from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from api.serializers import ReadLaterSerializer, HistorySerializer
from news.models import ReadLater, History

# Create your views here.
from rest_framework import viewsets


class ReadLaterViewSet(viewsets.ModelViewSet):
    queryset = ReadLater.objects.all()
    serializer_class = ReadLaterSerializer
    permission_classes = [IsAuthenticated]


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]
