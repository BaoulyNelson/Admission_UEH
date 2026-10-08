from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


def valider_taille_photo_profil(fichier):
    if fichier.size > 1024 * 1024:
        raise ValidationError("La taille maximale de la photo est de 1 Mo.")


class GestionnaireUtilisateur(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Une adresse e-mail est obligatoire.")
        utilisateur = self.model(email=self.normalize_email(email), **extra_fields)
        utilisateur.set_password(password)
        utilisateur.save(using=self._db)
        return utilisateur

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if not extra_fields["is_staff"] or not extra_fields["is_superuser"]:
            raise ValueError("Le superutilisateur doit avoir tous les droits.")
        return self.create_user(email, password, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("adresse e-mail", unique=True)
    prenom = models.CharField("prénom", max_length=100, blank=True)
    nom = models.CharField("nom", max_length=100, blank=True)
    photo_profil = models.FileField(
        "photo de profil",
        upload_to="photos_profils/%Y/%m/",
        blank=True,
        validators=[
            FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
            valider_taille_photo_profil,
        ],
    )
    is_staff = models.BooleanField("accès à l’administration", default=False)
    is_active = models.BooleanField("actif", default=True)
    date_inscription = models.DateTimeField("date d’inscription", auto_now_add=True)

    objects = GestionnaireUtilisateur()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.prenom} {self.nom}".strip()

    def get_short_name(self):
        return self.prenom or self.email
