from django import forms

from applications.comptes.models import Utilisateur


class FormulaireCreationUtilisateur(forms.ModelForm):
    mot_de_passe = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)
    confirmation_mot_de_passe = forms.CharField(
        label="Confirmation du mot de passe", widget=forms.PasswordInput
    )

    class Meta:
        model = Utilisateur
        fields = ["email", "prenom", "nom", "is_active"]

    def clean(self):
        donnees = super().clean()
        if donnees.get("mot_de_passe") != donnees.get("confirmation_mot_de_passe"):
            self.add_error(
                "confirmation_mot_de_passe",
                "Les deux mots de passe ne correspondent pas.",
            )
        return donnees

    def save(self, commit=True):
        utilisateur = super().save(commit=False)
        utilisateur.set_password(self.cleaned_data["mot_de_passe"])
        if commit:
            utilisateur.save()
        return utilisateur


class FormulaireModificationUtilisateur(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = [
            "email",
            "prenom",
            "nom",
            "is_active",
            "is_superuser",
            "groups",
            "user_permissions",
        ]


class FormulaireProfilAdministrateur(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ("prenom", "nom", "photo_profil")
        widgets = {
            "prenom": forms.TextInput(attrs={"autocomplete": "given-name"}),
            "nom": forms.TextInput(attrs={"autocomplete": "family-name"}),
            "photo_profil": forms.FileInput(
                attrs={
                    "accept": "image/jpeg,image/png,image/webp",
                    "data-apercu-photo-profil": "",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for champ in self.fields.values():
            champ.widget.attrs["class"] = "form-control"


class FormulaireInscription(forms.Form):
    field_order = ["email", "prenom", "nom", "password1", "password2"]

    prenom = forms.CharField(
        label="Prénom",
        max_length=100,
        widget=forms.TextInput(attrs={"autocomplete": "given-name"}),
    )
    nom = forms.CharField(
        label="Nom",
        max_length=100,
        widget=forms.TextInput(attrs={"autocomplete": "family-name"}),
    )

    def signup(self, request, user):
        user.prenom = self.cleaned_data["prenom"].strip()
        user.nom = self.cleaned_data["nom"].strip()
        user.save(update_fields=["prenom", "nom"])
