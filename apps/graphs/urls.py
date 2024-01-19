from django.urls import path
from .views import *

app_name = "graphs"

urlpatterns = [
    path("", DataItemListAPIView.as_view(), name="data_list"),
    path("create/", CreateAPIView.as_view(), name="data_create"),
    path("delete/<int:pk>/", DataItemDeleteAPIView.as_view(), name="data_delete"),
]
