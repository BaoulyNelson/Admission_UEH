from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string

from applications.candidatures.models import Inscription
from applications.candidatures.pdf import generer_pdf_inscription


def programmer_notification_validation_inscription(inscription_id):
    transaction.on_commit(
        lambda: envoyer_notification_validation_inscription.delay(inscription_id)
    )


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def envoyer_notification_validation_inscription(self, inscription_id):
    inscription = Inscription.objects.select_related(
        "candidat__utilisateur", "entite"
    ).get(pk=inscription_id)
    candidat = inscription.candidat.utilisateur
    nom_candidat = candidat.get_full_name() or candidat.email
    contexte = {
        "nom_candidat": nom_candidat,
        "entite": inscription.entite,
        "numero_dossier": inscription.numero_dossier,
        "annee_academique": inscription.annee_academique,
    }
    message = EmailMultiAlternatives(
        subject="Validation de votre inscription - UEH",
        body=render_to_string("notifications/validation_inscription.txt", contexte),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[candidat.email],
    )
    message.attach_alternative(
        render_to_string("notifications/validation_inscription.html", contexte),
        "text/html",
    )
    return message.send(fail_silently=False)


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def envoyer_confirmation_inscription(self, inscription_id):
    inscription = Inscription.objects.select_related(
        "candidat__utilisateur", "entite"
    ).get(pk=inscription_id)
    candidat = inscription.candidat.utilisateur
    courriel = EmailMessage(
        subject=f"Confirmation de votre dossier #{inscription.numero_dossier}",
        body=(
            f"Bonjour {candidat.prenom or candidat.email},\n\n"
            f"Votre candidature auprès de {inscription.entite} a été reçue.\n"
            f"Votre numéro de dossier est #{inscription.numero_dossier}.\n"
            "Connectez-vous à votre espace pour suivre son traitement."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[candidat.email],
    )
    courriel.attach(
        f"dossier-{inscription.numero_dossier}.pdf",
        generer_pdf_inscription(inscription),
        "application/pdf",
    )
    return courriel.send(fail_silently=False)
