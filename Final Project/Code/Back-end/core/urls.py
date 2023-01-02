from django.urls import path
from . import views

urlpatterns = [
    path("token/", views.CloudTokenObtainPairView.as_view()),
    path("update/", views.update)
]
