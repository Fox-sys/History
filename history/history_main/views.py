from django.shortcuts import render, redirect, get_object_or_404
from .models import MainUser, SolderPost, Exhibit
from django.views.generic import ListView, DetailView, View
from .forms import SolderForm, SignUpForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView

class SolderList(ListView):
    """
    View for serving list of solders
    """
    model = SolderPost
    template_name = "history_main/solder_list.html"

class SolderDetail(DetailView):
    """
    View for current solder
    """
    model = SolderPost
    template_name = "history_main/solder_detail.html"

class CreateUpdateSolder(View):
    """
    View for creating and updating solders
    """
    form_class = SolderForm
    model = SolderPost
    template_name = "history_main/solder_create.html"
    def get(self, request, **kwargs):
        """
        Get method for CreateUpdateSolder view.
        Takes one keyword arg for update method (pk)
        """
        form = self.form_class()
        print(kwargs)
        if "pk" in kwargs:
            obj = get_object_or_404(self.model, pk=kwargs['pk'])
            form = self.form_class(instance=obj)
        return render(request, self.template_name, context={"form": form})

    def post(self, request, **kwargs):
        """
        Post method for CreateUpdateSolder view.
        Takes one keyword arg for update method (pk).
        """
        instance = get_object_or_404(self.model, pk=kwargs['pk']) if "pk" in kwargs else None
        form = self.form_class(request.POST, request.FILES, instance=instance)
        form.instance.creator = MainUser.objects.get(id=1)
        if form.is_valid():
            form.save()
            return redirect('/')
        return render(request, self.template_name, context={"form": self.form_class(request.POST)})

   
def delete_solder(request, pk):
    """
    Delete method for solders.
    Takes one positional arg (pk).
    """
    post = get_object_or_404(SolderPost, pk=pk)
    if request.user.is_authenticated:
        if post.creator == request.user or request.user.is_staff or request.user.is_moderator or request.user.is_admin:
            post.delete()
    return redirect('/')


class Register(View):
    """
    View for user registration 
    """
    form_class = SignUpForm
    model = MainUser
    template_name = "registration/register.html"
    def get(self, request):
        """
        Get method for Register view
        """
        if request.user.is_authenticated:
            return redirect("/")
        form = self.form_class()
        return render(request, self.template_name, context={"form":form})

    def post(self, request):
        """
        Post method for Register view
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save() 
            user = authenticate(username=form.cleaned_data['username'], password=form.clean_password2())
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, context={"form":form})

class HLogoutView(LogoutView):
    """Logout view for users"""
    template_name = "registration/logout.html"


class ExhibitList(ListView):
    """
    View for serving list of exibits
    """
    model = Exhibit
    template_name = "history_main/exhibit_list.html"


class ExhibitDetail(DetailView):
    """
    View for current exhibit
    """
    model = Exhibit
    template_name = "history_main/exhibit_detail.html"