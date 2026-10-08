from mimetypes import guess_type

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render
from django.views import View

from applications.comptes.forms import FormulaireProfilAdministrateur
from applications.entites.models import AdministrateurEntite


class ProfilAdministrateurEntiteRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        if not AdministrateurEntite.objects.filter(utilisateur=request.user).exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ProfilAdministrateurEntiteView(ProfilAdministrateurEntiteRequiredMixin, View):
    def get(self, request):
        formulaire = FormulaireProfilAdministrateur(instance=request.user)
        return render(
            request,
            "comptes/profil_administrateur.html",
            {"formulaire": formulaire},
        )

    def post(self, request):
        formulaire = FormulaireProfilAdministrateur(
            request.POST,
            request.FILES,
            instance=request.user,
        )
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, "Votre profil a été mis à jour.")
            return redirect("comptes:profil_administrateur")
        return render(
            request,
            "comptes/profil_administrateur.html",
            {"formulaire": formulaire},
            status=400,
        )


class PhotoProfilAdministrateurView(ProfilAdministrateurEntiteRequiredMixin, View):
    def get(self, request):
        photo = request.user.photo_profil
        if not photo:
            raise Http404
        nom_fichier = photo.name.rsplit("/", 1)[-1]
        reponse = FileResponse(
            photo.open("rb"),
            as_attachment=False,
            filename=nom_fichier,
            content_type=guess_type(nom_fichier)[0] or "application/octet-stream",
        )
        reponse["Cache-Control"] = "private, no-store"
        reponse["X-Content-Type-Options"] = "nosniff"
        return reponse
