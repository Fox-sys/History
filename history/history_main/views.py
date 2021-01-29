from django.shortcuts import render, redirect, get_object_or_404
from .models import MainUser, SolderPost, Exhibit
from django.views.generic import ListView, DetailView, View, FormView
from .forms import SolderForm, SignUpForm, EditProfileForm
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
        if request.user.is_authenticated:
            form = self.form_class()
            if "pk" in kwargs:
                obj = get_object_or_404(self.model, pk=kwargs['pk'])
                form = self.form_class(instance=obj)
            return render(request, self.template_name, context={"form": form})
        return redirect('/')

    def post(self, request, **kwargs):
        """
        Post method for CreateUpdateSolder view.
        Takes one keyword arg for update method (pk).
        """
        if request.user.is_authenticated:
            instance = get_object_or_404(self.model, pk=kwargs['pk']) if "pk" in kwargs else None
            form = self.form_class(request.POST, request.FILES, instance=instance)
            form.instance.creator = MainUser.objects.get(id=request.user.id)
            if form.is_valid():
                obj = form.save()
                if instance is None:
                    request.user.uploads.add(obj)
                    request.user.uploads_amount += 1
                    request.user.save()
                return redirect('/')
            return render(request, self.template_name, context={"form": self.form_class(request.POST)})
        return redirect('/')
   
class AskDeleteSolder(View):
    """
    Delete view for solders.
    Takes one positional arg (pk).
    """
    template_name = "history_main/ask_delete.html"
    def get(self, request, pk):
        return render(request, self.template_name, context={"pk":pk})


class ConfirmDeleteSolder(View):
    """
    Confirm view for removing solder.
    Takes one positional arg (pk).
    """
    def get(self, request, pk):
        post = get_object_or_404(SolderPost, pk=pk)
        if request.user.is_authenticated:
            if post.creator == request.user or request.user.is_staff:
                if post.creator == request.user:
                    request.user.uploads.remove(post)
                    request.user.uploads_amount -= 1
                post.delete()
                request.user.save()
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
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save() 
            user = authenticate(username=form.cleaned_data['username'], password=form.clean_password2())
            login(request, user)
            return redirect('/')
        return render(request, self.template_name, context={"form":form})

class ConfirmLogoutView(LogoutView):
    """Logout view for users"""
    template_name = "registration/logout.html"
    

class AskLogoutView(View):
    template_name = "registration/ask_logout.html"
    def get(self, request):
        return render(request, self.template_name)


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


class ProfileDetail(DetailView):
    """
    View for current profile
    """
    model = MainUser
    template_name = "registration/profile_detail.html"


class ProfileList(ListView):
    """
    View for serving list of profiles
    """
    model = MainUser
    template_name = "registration/profile_list.html"

    def get_queryset(self):
        queryset = reversed(MainUser.objects.all().order_by("uploads_amount"))
        return queryset

class EditProfile(FormView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

