from django.urls import path
from .views import VendorRegisterAPIView

urlpatterns = [
    path("register/", VendorRegisterAPIView.as_view(), name="vendor-register"),
]