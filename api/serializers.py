from rest_framework import serializers

from news.models import ReadLater, History


#  HyperlinkedModelSerializer


class ReadLaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadLater
        fields = ['news']


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ['news']
