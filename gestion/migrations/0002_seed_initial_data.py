from django.db import migrations


def seed_initial_data(apps, schema_editor):
    Centre = apps.get_model("gestion", "Centre")
    Livre = apps.get_model("gestion", "Livre")

    livres = [
        {"code": "COMPAGNON", "nom": "Compagnon", "pages": 180, "prix": 1500},
        {"code": "ESSENTIEL", "nom": "Essentiel", "pages": 200, "prix": 2000},
        {"code": "VIATIQUE", "nom": "Viatique", "pages": 160, "prix": 1000},
        {"code": "ACTIVITES", "nom": "Activités", "pages": 120, "prix": 800},
    ]

    for l in livres:
        Livre.objects.get_or_create(
            code=l["code"],
            defaults={
                "nom": l["nom"],
                "pages": l["pages"],
                "prix_unitaire_defaut": l["prix"],
            },
        )

    centre_noms = [
        "YAMOUSSOKRO",
        "OUSTAZ KONATE",
        "DIENG AISSATA",
        "TANTA HIDAYA",
        "port bouet",
        "IQRA",
        "SELMER",
        "kor",
        "daloa",
        "OUSTAZ DALOA",
        "AVICENNE",
        "MARCORY",
        "BOUAKE 1",
        "ABOBO",
        "mpouto",
        "aeroport",
    ]

    for nom in centre_noms:
        Centre.objects.get_or_create(nom=nom)


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_initial_data),
    ]
