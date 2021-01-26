from django.urls import path
from .views import SolderList, SolderDetail

urlpatterns = [
    path('', SolderList.as_view(), name="index"),
    path('solders/<int:pk>/', SolderDetail.as_view(), name="solder_detail"),
]
