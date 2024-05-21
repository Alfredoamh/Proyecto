from django.urls import path
from ReportsApp import views

urlpatterns = [
    path("", views.ReportView.as_view(), name="Reports"),
    path("generate_pdf/<pk>/", views.GenerarPdfView.as_view(), name="generate_pdf"),
    path("lista/", views.ReportListView.as_view(), name="ReportList"),
    path("graficos/", views.ChartsView.as_view(), name="Charts"),
]
