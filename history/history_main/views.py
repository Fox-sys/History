from django.shortcuts import render, redirect, get_object_or_404
from .models import MainUser, SolderPost, Exhibit
from django.views.generic import ListView, DetailView, View, FormView
from .forms import SolderForm, SignUpForm, EditProfileForm, ChangePasswordForm, GetUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.conf import settings

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


class ConfirmDeleteSolder(View):
    """
    Confirm view for removing solder.
    Takes one positional arg (pk).
    """
    def get(self, request, pk):
        post = get_object_or_404(SolderPost, pk=pk)
        if request.user.is_authenticated:
            if post.creator == request.user or request.user.is_staff:
                post.creator.uploads_amount -= 1
                post.creator.save()
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


class ChangePasswordView(FormView):
    form_class_get_user = GetUserForm
    form_class_change_password = ChangePasswordForm
    template_name_get_user = 'registration/get_username.html'
    template_name_change_password = "registration/change_password.html"

    def get(self, request):
        return render(request, self.template_name_get_user, context={"form": self.form_class_get_user()})

    def post(self, request):
        if "user" in request.POST:
            form = self.form_class_change_password(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/login')
        else:
            form = self.form_class_get_user(request.POST)
            if form.is_valid():
                user = get_object_or_404(MainUser, username=form.get_username())
                send_mail(f'Сброс пароля', f"Секретныый ключ: {user.secret_key}",
                                    settings.DEFAULT_FROM_EMAIL, [user.email])
                return render(request, self.template_name_change_password, context={"user": user})
            return render(request, self.template_name_get_user, context={"form": form})


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
    """
    View for editing profile
    """
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, context={'form': form})


    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user)
        if form.is_valid:
            form.save()
        return redirect(request.user.get_absolute_url())

