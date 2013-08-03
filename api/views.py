from api.models import Package
from django.http import Http404
from rest_framework import serializers
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView


class PackageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Package
        fields = ("name", "url", )


class PackagesListView(ListCreateAPIView):
    model = Package


class PackagesFindView(RetrieveAPIView):
    model = Package
    serializer_class = PackageSerializer

    def get_object(self):
        try:
            return self.model.objects.get(name=self.kwargs['name'])
        except Package.DoesNotExist:
            raise Http404
