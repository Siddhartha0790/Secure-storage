from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import EncryptedFileUploadSerializer
from django.shortcuts import get_object_or_404
from django.http import FileResponse

class EncryptedFileUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EncryptedFileUploadSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "File uploaded successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
from rest_framework.generics import ListAPIView
from .models import EncryptedFile
from .serializers import EncryptedFileListSerializer

class EncryptedFileListView(ListAPIView):
    serializer_class = EncryptedFileListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EncryptedFile.objects.filter(user=self.request.user)



class EncryptedFileDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        encrypted_file = get_object_or_404(
            EncryptedFile,
            id=file_id,
            user=request.user
        )

        response = FileResponse(
            encrypted_file.file.open('rb'),
            as_attachment=True,
            filename=encrypted_file.original_filename
           
        )
        return response
    
    
import base64
class EncryptedFileMetaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id):
        encrypted_file = get_object_or_404(
            EncryptedFile,
            id=file_id,
            user=request.user
        )

        return Response({
            "id": encrypted_file.id,
            "original_filename": encrypted_file.original_filename,
            "size": encrypted_file.size,
            "encrypted_key": base64.b64encode(encrypted_file.encrypted_key).decode(),
            "iv": base64.b64encode(encrypted_file.iv).decode()
        })