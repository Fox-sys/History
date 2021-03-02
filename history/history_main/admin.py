from django.contrib import admin
from .models import SolderPost, MainUser, Exhibit
from django.contrib.auth.admin import UserAdmin

@admin.register(MainUser)
class MainUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'middle_name', 'phone', 'email', 'uploads_amount', 'email_is_hidden', 'phone_is_hidden', 'avatar', 'secret_key')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'groups', 'user_permissions', 'is_moderator', 'is_admin'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'middle_name', 'phone', 'uploads_amount', 'email_is_hidden', 'phone_is_hidden', 'avatar', 'is_moderator', 'is_admin', 'secret_key')
    list_filter = ('is_staff', 'is_active', 'groups',)
    filter_horizontal = ('groups', 'user_permissions', 'uploads')


admin.site.register(SolderPost)
admin.site.register(Exhibit)
