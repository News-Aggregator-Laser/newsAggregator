from rest_framework import serializers

from news.models import ReadLater, History


#  HyperlinkedModelSerializer


class ReadLaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadLater
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
