# Admission UEH

Portail Django de dépôt et de suivi des candidatures aux concours de l’Université d’État d’Haïti.

## Installation locale

Prévoir Python 3.12. Depuis PowerShell :

```powershell
python3 -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Le profil local utilise SQLite, affiche les courriels dans le terminal et traite les tâches Celery immédiatement. Les commandes habituelles suffisent :

```powershell
python manage.py migrate
python manage.py importer_entites
python manage.py createsuperuser
python manage.py runserver
```

Le portail local est disponible à `http://127.0.0.1:8000/`. Les emails et PDFs sont traités en mode local; les emails de confirmation s’affichent dans le terminal.

Pour un déploiement MySQL/MariaDB, prévoir aussi Redis, créer une base `admission_ueh` et renseigner `.env`. Utiliser explicitement la configuration de production pour les commandes d’administration :

```powershell
python manage.py migrate --settings=configuration.settings
python manage.py importer_entites --settings=configuration.settings
python manage.py createsuperuser --settings=configuration.settings
```

La commande importe ou met à jour `data/entites.csv` (colonnes `code,nom,email`). Les nouvelles entités arrivent avec les inscriptions ouvertes; un superutilisateur peut fermer/réouvrir les inscriptions et activer/désactiver chaque entité dans l’administration. Une inscription fermée est visible sur la page publique mais impossible à soumettre.

Dans un second terminal, démarrer les tâches asynchrones (emails de confirmation avec reçu PDF) :

```powershell
.\venv\Scripts\Activate.ps1
celery -A configuration worker -l info --pool=solo
```

L’interface d’administration est disponible sur `/admin/`; la documentation API Swagger sur `/api/docs/`.

## Administrateur d’entité

1. Se connecter à `/admin/` avec le superutilisateur.
2. Créer l’entité, ses options, ses salles et ses horaires AM/PM.
3. Créer un utilisateur avec une adresse professionnelle, un mot de passe sûr et « accès à l’administration » activé.
4. Ajouter un enregistrement « Administrateur d’entité » reliant cet utilisateur à une seule entité.

L’administrateur voit uniquement les dossiers de l’entité liée. Un compte sans entité n’accède pas à `/admin/`; seul un superutilisateur peut administrer toutes les entités.

## Tests

Les tests locaux utilisent SQLite sans modifier la configuration MySQL de production :

```powershell
python manage.py test applications.candidatures.tests applications.candidatures.tests_securite applications.documents.tests --settings=configuration.test_settings
```

Le test de concurrence requiert MySQL/InnoDB, car SQLite ne fournit pas le verrou `SELECT FOR UPDATE` nécessaire.