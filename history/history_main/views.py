from django.shortcuts import render, redirect, get_object_or_404
from .models import MainUser, SolderPost, Exhibit
from django.views.generic import ListView, DetailView, View
from .forms import SolderForm, SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView

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

   
def delete_solder(request, pk):
    post = get_object_or_404(SolderPost, pk=pk)
    if request.user.is_authenticated:
        if post.creator == request.user or request.user.is_staff or request.user.is_moderator or request.user.is_admin:
            post.delete()
    return redirect('/')


class Register(View):
    form_class = SignUpForm
    model = MainUser
    template_name = "registration/register.html"
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("/")
        form = self.form_class()
        return render(request, self.template_name, context={"form":form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save() 
            user = authenticate(username=form.cleaned_data['username'], password=form.clean_password2())
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, context={"form":form})

class HLogoutView(LogoutView):
    template_name = "registration/logout.html"