from rest_framework import serializers


class StopsSerializer(serializers.Serializer):
    name = serializers.CharField()


class ShortestRouteSerializer(serializers.Serializer):
    distance = serializers.IntegerField()
    route = StopsSerializer(many=True)
