from django.urls import path
from .views import SolderList, SolderDetail, CreateUpdateSolder

urlpatterns = [
    path('', SolderList.as_view(), name="index"),
    path('solders/<int:pk>/', SolderDetail.as_view(), name="solder_detail"),
    path('solders/create/', CreateUpdateSolder.as_view(), name="create_solder"),
    path('solders/update/<int:pk>', CreateUpdateSolder.as_view(), name="create_solder"),
]
