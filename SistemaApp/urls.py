from django.urls import path
from SistemaApp import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="Home"),
    path("usuarios/", views.UsuariosView.as_view(), name="Usuarios"),
]
