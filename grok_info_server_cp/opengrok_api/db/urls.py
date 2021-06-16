# db/urls.py

from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import SpView, BuildView

sp_list = SpView.as_view({
        'post': 'create',
        'get': 'list'
})

sp_detail = SpView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
})
build_list = BuildView.as_view({
        'post': 'create',
        'get': 'list'
})

build_detail = BuildView.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
        path('auth/', include('rest_framework.urls',
                namespace='rest_framework')),
        path('sp/', sp_list, name='sp_list'),
        path('sp/<int:pk>/', sp_detail, name='sp_detail'),
        path('build/', build_list, name='build_list'),
        path('build/<int:pk>/', build_detail, name='build_detail'),
])
