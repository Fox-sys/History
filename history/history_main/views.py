from django.shortcuts import render, redirect, get_object_or_404
from .models import MainUser, SolderPost, Exhibit
from django.views.generic import ListView, DetailView, View
from .forms import SolderForm

class SolderList(ListView):
    model = SolderPost
    template_name = "history_main/solder_list.html"

class SolderDetail(DetailView):
    model = SolderPost
    template_name = "history_main/solder_detail.html"

class CreateUpdateSolder(View):
    form_class = SolderForm
    model = SolderPost
    template_name = "history_main/solder_create.html"
    def get(self, request, **kwargs):
        form = self.form_class()
        print(kwargs)
        if "pk" in kwargs:
            obj = get_object_or_404(self.model, pk=kwargs['pk'])
            form = self.form_class(instance=obj)
        return render(request, self.template_name, context={"form": form})

    def post(self, request, **kwargs):
        instance = get_object_or_404(self.model, pk=kwargs['pk']) if "pk" in kwargs else None
        form = self.form_class(request.POST, request.FILES, instance=instance)
        form.instance.creator = MainUser.objects.get(id=1)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, self.template_name, context={"form": self.form_class(request.POST)})

    
