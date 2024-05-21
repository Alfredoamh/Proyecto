from django.urls import path
from DocumentoApp import views

urlpatterns = [
    path("", views.DocumentView.as_view(), name="Documents"),
    path("data_documents/", views.DataDocumentsView.as_view(), name="DataDocuments"),
]
