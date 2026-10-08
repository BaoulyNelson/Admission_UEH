from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/", include("applications.candidatures.api_urls")),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("", include("applications.tableau_bord.urls")),
    path("candidatures/", include("applications.candidatures.urls")),
    path("candidats/", include("applications.candidats.urls")),
    path("documents/", include("applications.documents.urls")),
    path("resultats/", include("applications.resultats.urls")),
    path("gestion/", include("applications.administration.urls")),
    path("comptes/", include("applications.comptes.urls")),
    path("comptes/", include("allauth.urls")),
]
