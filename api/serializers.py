from rest_framework import serializers

from news.models import ReadLater, History, Like, Comment, Subscription


#  HyperlinkedModelSerializer


class ReadLaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadLater
        fields = ['news']


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['news']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['news']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['news', 'content']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['email']
