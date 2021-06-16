# db/serializers.py

from rest_framework import serializers
from .models import Sp, Build

class SpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sp
        fields = [
            'id',
            'name',
            'version',
            'category',
            'wiki',
            'description',
            'project_name'
        ]
    def create(self, validated_data):
        return Sp.objects.create(**validated_data)
class BuildSerializer(serializers.ModelSerializer):
    class Meta:
        model = Build
        fields = [
            'id',
            'sp_id_fk',
            'name',
            'wiki',
            'release_note',
            'fastboot',
            'qfil',
            'status',
            'release_date',
            'apps_id',
            'au_tag',
            'gvm_id',
        ]
    def create(self, validated_data):
        return Build.objects.create(**validated_data)

