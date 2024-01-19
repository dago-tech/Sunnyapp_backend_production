from django.urls import path
from .views import *

app_name = "users"

urlpatterns = [
    path("", UserListAPIView.as_view(), name="user_list"),
    path("create/", UserCreateAPIView.as_view(), name="user_create"),
    path(
        "get_user_email/<int:user_id>/",
        GetUserEmailAPIView.as_view(),
        name="user_email",
    ),
    path("logout/blacklist/", BlacklistTokenUpdateView.as_view(), name="blacklist"),
]
