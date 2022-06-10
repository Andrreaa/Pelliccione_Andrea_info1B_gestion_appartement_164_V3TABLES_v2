"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms import SubmitField
from wtforms.validators import Length, InputRequired, DataRequired
from wtforms.validators import Regexp


class FormWTFAjouterGenres(FlaskForm):
    """
        Dans le formulaire "personne_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_personne_wtf = StringField("Clavioter le nom", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                      Regexp(nom_genre_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                      ])
    prenom_personne_wtf = StringField("Clavioter le prenom ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                      Regexp(nom_genre_regexp,
                                                                             message="Pas de chiffres, de caractères "
                                                                                     "spéciaux, "
                                                                                     "d'espace à double, de double "
                                                                                     "apostrophe, de double trait union")
                                                                      ])
    Date_naissance_personne_wtf = DateField("Clavioter la date de naisssance ")



    submit = SubmitField("Enregistrer personnes")


class FormWTFUpdateGenre(FlaskForm):
    """
        Dans le formulaire "personne_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    nom_genre_update_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_personne_update_wtf = StringField("Modifié le nom ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(nom_genre_update_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    prenom_personne_update_wtf = StringField("Modifié le prenom ",
                                          validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                      Regexp(nom_genre_update_regexp,
                                                             message="Pas de chiffres, de "
                                                                     "caractères "
                                                                     "spéciaux, "
                                                                     "d'espace à double, de double "
                                                                     "apostrophe, de double trait "
                                                                     "union")
                                                      ])
    Date_naissance_personne_wtf = DateField("Modifié date naissance", validators=[InputRequired("Date obligatoire"),
                                                               DataRequired("Date non valide")])
    submit = SubmitField("Update personnes")


class FormWTFDeleteGenre(FlaskForm):
    """
        Dans le formulaire "personne_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_personne".
    """
    nom_genre_delete_wtf = StringField("Effacer cette personnes")
    prenom_genre_delete_wtf = StringField("")
    date_genre_delete_wtf = DateField("")
    submit_btn_del = SubmitField("Effacer personnes")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
