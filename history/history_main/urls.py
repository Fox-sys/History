from django.urls import path
from .views import SolderList, SolderDetail, CreateUpdateSolder, \
                   DeleteSolder, Register, HLogoutView, \
                   ExhibitDetail, ExhibitList, ProfileDetail, \
                   ProfileList, ConfirmDeleteSolder

urlpatterns = [
    path('', SolderList.as_view(), name="index"),
    path('solders/<int:pk>/', SolderDetail.as_view(), name="solder_detail"),
    path('solders/create/', CreateUpdateSolder.as_view(), name="create_solder"),
    path('solders/update/<int:pk>/', CreateUpdateSolder.as_view(), name="create_solder"),
    path('solders/delete/<int:pk>/', DeleteSolder.as_view(), name="delete_solder"),
    path('solders/delete/<int:pk>/confirm/', ConfirmDeleteSolder.as_view(), name="confirm_delete_solder"),
    path('accounts/register/', Register.as_view(), name="register"),
    path('accounts/logout/', HLogoutView.as_view(), name="logout"),
    path('exhibits/', ExhibitList.as_view(), name="exhibit_list"),
    path('exhibits/<int:pk>', ExhibitDetail.as_view(), name="exhibit_detail"),
    path('profiles/<int:pk>', ProfileDetail.as_view(), name="profile_detail"),
    path('profiles/', ProfileList.as_view(), name="profile_list"),
]
