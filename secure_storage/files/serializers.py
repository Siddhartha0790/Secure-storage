from rest_framework import serializers
from .models import EncryptedFile

import base64
from rest_framework import serializers
from .models import EncryptedFile

class EncryptedFileUploadSerializer(serializers.ModelSerializer):
    encrypted_key = serializers.CharField()
    iv = serializers.CharField()

    class Meta:
        model = EncryptedFile
        fields = [
            "file",
            "encrypted_key",
            "iv",
            "original_filename",
            "size",
        ]

    def create(self, validated_data):
        # 🔐 Base64 decode crypto fields
        encrypted_key_b64 = validated_data.pop("encrypted_key")
        iv_b64 = validated_data.pop("iv")

        encrypted_key = base64.b64decode(encrypted_key_b64)
        iv = base64.b64decode(iv_b64)

        return EncryptedFile.objects.create(
            encrypted_key=encrypted_key,
            iv=iv,
            **validated_data
        )


class EncryptedFileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncryptedFile
        fields = [
            'id',
            'original_filename',
            'size',
            'created_at',
        ]