from django.shortcuts import render, redirect, get_object_or_404
from .models import MainUser, SolderPost, Exhibit
from django.views.generic import ListView, DetailView, View, FormView
from .forms import SolderForm, SignUpForm, EditProfileForm, ChangePasswordForm, GetUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LogoutView
from django.core.mail import send_mail
from django.conf import settings
import logging

LVLS = ["INFO", "WARNING", "ERROR"]

LOGGER = logging.getLogger(__name__)

def get_logger_template(lvl, message):
    return f"[{LVLS[lvl]}] - {message}"

class ListPagerView(ListView):
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = int(self.request.GET.get('page', '1'))
        context['total'] = (self.get_queryset().count() // self.paginate_by) + 1 
        context['next'] = context['page']+1 
        context['last'] = context['page']-1 
        return context


class SolderList(ListPagerView):
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
                black_list_errors = form.black_list_validated()
                if black_list_errors is None:
                    obj = form.save()
                    if instance is None:
                        request.user.uploads.add(obj)
                        request.user.uploads_amount += 1
                        request.user.save()
                        LOGGER.info(get_logger_template(0, f"Created solder with id {obj.id}"))
                    else:
                        LOGGER.info(get_logger_template(0, f"Updated solder with id {obj.id}"))
                    return redirect('/')
                return render(request, self.template_name, context={"message": black_list_errors})
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
                LOGGER.info(get_logger_template(0, f'deleted solder by {request.user.id}'))
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
            LOGGER.info(get_logger_template(0, f'Created new user name: {user.first_name} {user.last_name}'))
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
                obj = form.save()
                if obj:
                    logging.info(get_logger_template(0, f"Был изменён пароль для пользователя: {obj.id}"))
                    return redirect('/login')
        else:
            form = self.form_class_get_user(request.POST)
            if form.is_valid():
                user = get_object_or_404(MainUser, username=form.get_username())
                send_mail(f'Сброс пароля', f"Секретныый ключ: {user.secret_key}",
                                    settings.DEFAULT_FROM_EMAIL, [user.email])
                return render(request, self.template_name_change_password, context={"user": user})
            return render(request, self.template_name_get_user, context={"form": form})
        return render(request, self.template_name_change_password, context={"form": self.form_class_change_password(), "message": "Неверный ключ или пароли не совпадают"})


class ExhibitList(ListPagerView):
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


class ProfileList(ListPagerView):
    """
    View for serving list of profiles
    """
    model = MainUser
    template_name = "registration/profile_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("-uploads_amount")
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
