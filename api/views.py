import base64
from rest_framework import status
# Create your views here.
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.serializers import ReadLaterSerializer, HistorySerializer, LikeSerializer, CommentSerializer, SubscriptionSerializer
from news.models import ReadLater, History, Like, Comment, Subscription


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
        read_later = ReadLater.objects.filter(user=request.user, news_id=request.data["news"]).update(is_removed=False)
        if not read_later:
            read_later = ReadLater.objects.create(user=request.user, news_id=request.data["news"])
            read_later.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        news_id = kwargs.get("pk")
        ReadLater.objects.filter(user=request.user, news=news_id).update(is_removed=True)
        return Response(status=status.HTTP_201_CREATED)


class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        history = History.objects.filter(user=request.user, news_id=request.data["news"]).update(is_removed=False)
        if not history:
            history = History.objects.create(user=request.user, news_id=request.data["news"])
            history.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        news_id = kwargs.get("pk")
        History.objects.filter(user=request.user, news=news_id).update(is_removed=True)
        return Response(status=status.HTTP_201_CREATED)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


def decode(code):
    return base64.b64decode(code).decode("utf-8")


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        subscription = Subscription.objects.filter(email=request.data["email"]).update(is_subscribed=True)
        if not subscription:
            subscription = Subscription.objects.create(email=request.data["email"])
            subscription.save()
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        subscription_id = kwargs.get("pk")
        Subscription.objects.filter(email=decode(subscription_id)).update(is_subscribed=False)
        return Response(status=status.HTTP_201_CREATED)
