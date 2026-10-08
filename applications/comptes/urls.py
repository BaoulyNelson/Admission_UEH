from django.urls import path

from applications.comptes.views import (
    PhotoProfilAdministrateurView,
    ProfilAdministrateurEntiteView,
)

app_name = "comptes"
urlpatterns = [
    path(
        "mon-profil/",
        ProfilAdministrateurEntiteView.as_view(),
        name="profil_administrateur",
    ),
    path("photo-profil/", PhotoProfilAdministrateurView.as_view(), name="photo_profil"),
]
