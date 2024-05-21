from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

# Create your views here.


class HomeView(LoginRequiredMixin, ListView):
    model = User
    template_name = "pages/index.html"

    def get_queryset(self):
        return User.objects.order_by('-last_login')[:4]


class UsuariosView(LoginRequiredMixin, ListView):
    model = User
    template_name = "pages/usuarios.html"
