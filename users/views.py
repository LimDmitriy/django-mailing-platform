from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from users.models import User


class RegisterView(CreateView):
    model = User
    success_url = reverse_lazy("catalog:product_list")

