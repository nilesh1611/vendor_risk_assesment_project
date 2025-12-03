from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/banks/", include("banks.urls")),
    path("api/vendors/", include("vendors.urls")),
    path("api/questionnaire/", include("questionnaire.urls")),
    path("api/submissions/", include("submissions.urls")),
]