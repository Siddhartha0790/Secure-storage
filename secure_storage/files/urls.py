from django.urls import path
from .views import EncryptedFileUploadView,EncryptedFileListView,EncryptedFileDownloadView,EncryptedFileMetaView

urlpatterns = [
    path('upload/', EncryptedFileUploadView.as_view()),
    path('', EncryptedFileListView.as_view()),
    path('<int:file_id>/download/', EncryptedFileDownloadView.as_view()),
    path('<int:file_id>/meta/', EncryptedFileMetaView.as_view()),

    

]
