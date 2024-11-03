from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    img_content = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Document
        fields = ['id', 'title', 'content', 'img_content', 'created_at']
        read_only_fields = ['created_at']