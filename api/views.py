from api.models import Package
from django.http import Http404
from rest_framework import serializers
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView


class PackageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Package
        fields = ("name", "url", )


class PackagesListView(ListCreateAPIView):
    model = Package


class PackagesSearchView(ListAPIView):
    model = Package

    def get_queryset(self):
        search = self.kwargs['name']
        return self.model.objects.filter(name__icontains=search)


class PackagesFindView(RetrieveAPIView):
    model = Package
    serializer_class = PackageSerializer

    def get_object(self):
        try:
            return self.model.objects.get(name=self.kwargs['name'])
        except Package.DoesNotExist:
            raise Http404
