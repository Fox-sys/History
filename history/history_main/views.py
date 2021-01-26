from django.shortcuts import render
from .models import MainUser, SolderPost, Exhibit
from django.views.generic import ListView, DetailView, View

class SolderList(ListView):
    model = SolderPost
    template_name = "history_main/solder_list.html"

class SolderDetail(DetailView):
    model = SolderPost
    template_name = "history_main/solder_detail.html"
