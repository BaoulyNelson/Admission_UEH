import applications.comptes.models
from django.core.validators import FileExtensionValidator
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("comptes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="utilisateur",
            name="photo_profil",
            field=models.FileField(
                blank=True,
                upload_to="photos_profils/%Y/%m/",
                validators=[
                    FileExtensionValidator(["jpg", "jpeg", "png", "webp"]),
                    applications.comptes.models.valider_taille_photo_profil,
                ],
                verbose_name="photo de profil",
            ),
        ),
    ]