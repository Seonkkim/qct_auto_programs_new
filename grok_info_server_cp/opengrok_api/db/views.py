from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from .serializers import SpSerializer, BuildSerializer
from .models import Sp, Build
from url_filter.integrations.drf import DjangoFilterBackend


class SpView(viewsets.ModelViewSet):
    queryset = Sp.objects.all()
    serializer_class = SpSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['category', 'version', 'project_name']

#permission_classes = (permissions.IsAuthenticated,)
#def perform_create(self, serializer):
#       serializer.save(user=self.request.user)
class BuildView(viewsets.ModelViewSet):
    queryset = Build.objects.all()
    serializer_class = BuildSerializer
#permission_classes = (permissions.IsAuthenticated,)
#    def perform_create(self, serializer):
#       serializer.save(user=self.request.user)


