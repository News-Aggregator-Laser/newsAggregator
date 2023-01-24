from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.serializers import ReadLaterSerializer, HistorySerializer
from news.models import ReadLater, History

# Create your views here.
from rest_framework import viewsets


class ReadLaterViewSet(viewsets.ModelViewSet):
    queryset = ReadLater.objects.all()
    serializer_class = ReadLaterSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # serializer.save(user=request.user)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        read_later = ReadLater.objects.filter(
            user=request.user, news_id=request.data["news"]
        ).update(is_removed=False)
        if not read_later:
            read_later = ReadLater.objects.create(
                user=request.user, news_id=request.data["news"]
            )
            read_later.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        news_id = kwargs.get("pk")
        ReadLater.objects.filter(user=request.user, news=news_id).update(
            is_removed=True
        )
        return Response(status=status.HTTP_201_CREATED)


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def destroy(self, request, *args, **kwargs):
        news_id = kwargs.get("pk")
        History.objects.filter(user=request.user, news=news_id).delete()
        return Response(status=status.HTTP_201_CREATED)
