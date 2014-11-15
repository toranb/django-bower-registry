from api.models import Package
from django.http import Http404
from rest_framework import serializers
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView


class PackageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Package
        fields = ("name", "url", )


class PackagesListView(ListCreateAPIView):
    model = Package
    serializer_class = PackageSerializer


class PackagesSearchView(ListAPIView):
    serializer_class = PackageSerializer

    def get_queryset(self):
        search = self.kwargs['name']
        return Package.objects.filter(name__icontains=search)


class PackagesFindView(RetrieveUpdateAPIView):
    serializer_class = PackageSerializer

    def get_object(self):
        try:
            return Package.objects.get(name=self.kwargs['name'])
        except Package.DoesNotExist:
            raise Http404
