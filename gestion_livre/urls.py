# gestion_livre/urls.py
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from gestion.views import (
    dashboard,
    releve_list,
    releve_create,
    rapport_hebdomadaire,
    rapport_trimestriel,
    rapport_mensuel,
    rapport_annuel,
    rapport_global,
    export_rapport_mensuel_excel,
    export_rapport_trimestriel_excel,
    export_rapport_annuel_excel,
    export_rapport_global_excel,
    export_rapport_mensuel_pdf,
    export_rapport_trimestriel_pdf,
    export_rapport_annuel_pdf,
    livre_list,
    livre_create,
    livre_update,
    livre_delete,
    centre_list,
    centre_create,
    centre_update,
    centre_delete,
)



urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="accounts/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Dashboard
    path("", dashboard, name="dashboard"),

    # Relevés
    path("releves/", releve_list, name="releve_list"),
    path("releves/nouveau/", releve_create, name="releve_create"),

    # Rapports
    path("rapports/mois/", rapport_mensuel, name="rapport_mensuel"),
    path(
        "rapports/mois/export-excel/",
        export_rapport_mensuel_excel,
        name="export_rapport_mensuel_excel",
    ),
    path(
        "rapports/mois/export-pdf/",
        export_rapport_mensuel_pdf,
        name="export_rapport_mensuel_pdf",
    ),

    path("rapports/semaine/", rapport_hebdomadaire, name="rapport_hebdomadaire"),
    path("rapports/global/", rapport_global, name="rapport_global"),
    path(
        "rapports/global/export-excel/",
        export_rapport_global_excel,
        name="export_rapport_global_excel",
    ),

    path("rapports/trimestre/", rapport_trimestriel, name="rapport_trimestriel"),
    path(
        "rapports/trimestre/export-excel/",
        export_rapport_trimestriel_excel,
        name="export_rapport_trimestriel_excel",
    ),
    path(
        "rapports/trimestre/export-pdf/",
        export_rapport_trimestriel_pdf,
        name="export_rapport_trimestriel_pdf",
    ),

    path("rapports/annee/", rapport_annuel, name="rapport_annuel"),
    path(
        "rapports/annee/export-excel/",
        export_rapport_annuel_excel,
        name="export_rapport_annuel_excel",
    ),
    path(
        "rapports/annee/export-pdf/",
        export_rapport_annuel_pdf,
        name="export_rapport_annuel_pdf",
    ),

    # Livres (CRUD admin)
    path("livres/", livre_list, name="livre_list"),
    path("livres/nouveau/", livre_create, name="livre_create"),
    path("livres/<int:pk>/modifier/", livre_update, name="livre_update"),
    path("livres/<int:pk>/supprimer/", livre_delete, name="livre_delete"),

    # Centres (CRUD admin)
    path("centres/", centre_list, name="centre_list"),
    path("centres/nouveau/", centre_create, name="centre_create"),
    path("centres/<int:pk>/modifier/", centre_update, name="centre_update"),
    path("centres/<int:pk>/supprimer/", centre_delete, name="centre_delete"),


]
