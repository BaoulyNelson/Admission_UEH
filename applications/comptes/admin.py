from django.contrib import admin
from allauth.account.models import EmailAddress

from applications.comptes.forms import (
    FormulaireCreationUtilisateur,
    FormulaireModificationUtilisateur,
)
from applications.comptes.models import Utilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    add_form = FormulaireCreationUtilisateur
    form = FormulaireModificationUtilisateur
    list_display = ("email", "prenom", "nom", "is_active", "is_superuser")
    list_filter = ("is_active", "is_superuser")
    search_fields = ("email", "prenom", "nom")
    ordering = ("email",)
    filter_horizontal = ("groups", "user_permissions")
    actions = ("delete_selected", "activer_utilisateurs", "desactiver_utilisateurs")

    @admin.action(description="Activer les comptes sélectionnés")
    def activer_utilisateurs(self, request, queryset):
        nombre = queryset.update(is_active=True)
        self.message_user(request, f"{nombre} compte(s) activé(s).")

    @admin.action(description="Désactiver les comptes sélectionnés")
    def desactiver_utilisateurs(self, request, queryset):
        comptes_a_desactiver = queryset.exclude(pk=request.user.pk)
        nombre = comptes_a_desactiver.update(is_active=False)
        if queryset.filter(pk=request.user.pk).exists():
            self.message_user(
                request,
                f"{nombre} compte(s) désactivé(s); votre propre compte a été conservé actif.",
                level="WARNING",
            )
        else:
            self.message_user(request, f"{nombre} compte(s) désactivé(s).")

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return [
                (
                    None,
                    {
                        "fields": (
                            "email",
                            "prenom",
                            "nom",
                            "mot_de_passe",
                            "confirmation_mot_de_passe",
                            "is_active",
                        )
                    },
                )
            ]
        return [
            (
                None,
                {
                    "fields": (
                        "email",
                        "prenom",
                        "nom",
                        "is_active",
                        "is_superuser",
                        "groups",
                        "user_permissions",
                    )
                },
            )
        ]

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs["form"] = self.form if obj else self.add_form
        return super().get_form(request, obj, change, **kwargs)

    def has_module_permission(self, request):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            EmailAddress.objects.update_or_create(
                user=obj,
                email=obj.email,
                defaults={"primary": True, "verified": True},
            )
