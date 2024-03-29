"""Gestion des "routes" FLASK et des données pour les personnes.
Fichier : gestion_genres_crud.py
Auteur : OM 2021.03.16
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164 import app
from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.droits.gestion_genres_wtf_forms import FormWTFAjouterGenres
from APP_FILMS_164.droits.gestion_genres_wtf_forms import FormWTFDeleteGenre
from APP_FILMS_164.droits.gestion_genres_wtf_forms import FormWTFUpdateGenre

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /genres_afficher
    
    Test : ex : http://127.0.0.1:5005/genres_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les personnes.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@app.route("/genres_afficher/<string:order_by>/<int:id_genre_sel>", methods=['GET', 'POST'])
def genres_afficher(order_by, id_genre_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_genre_sel == 0:
                    strsql_droit_afficher = """SELECT Id_personne, Nom_personne, Prenom_personne, Date_naissance_personne FROM t_personne ORDER BY Id_personne ASC"""
                    mc_afficher.execute(strsql_droit_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_personne"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_genre_selected": id_genre_sel}
                    strsql_droit_afficher = """SELECT Id_personne, Nom_personne, Prenom_personne, Date_naissance_personne FROM t_personne WHERE Id_personne = %(value_id_genre_selected)s"""

                    mc_afficher.execute(strsql_droit_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_droit_afficher = """SELECT Id_personne, Nom_personne, Prenom_personne, Date_naissance_personne FROM t_personne ORDER BY Id_personne DESC"""

                    mc_afficher.execute(strsql_droit_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_genre_sel == 0:
                    flash("""La table "t_personne" est vide. !!""", "warning")
                elif not data_genres and id_genre_sel > 0:
                    # Si l'utilisateur change l'Id_personne dans l'URL et que le genre n'existe pas,
                    flash(f"Le personnes demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_personne" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données personnes affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{genres_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("personnes/personne_afficher.html", data=data_genres)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genre_ajouter
    
    Test : ex : http://127.0.0.1:5005/genre_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un adresse
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "personnes/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genres_ajouter", methods=['GET', 'POST'])
def genres_ajouter_wtf():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            if form.validate_on_submit():
                nom_personne = form.nom_personne_wtf.data
                prenom_personne = form.prenom_personne_wtf.data
                Date_naissance_personne = form.Date_naissance_personne_wtf.data
                valeurs_insertion_dictionnaire = {"value_nom_personne": nom_personne,
                                                  "value_prenom_personne": prenom_personne,
                                                  "value_Date_naissance_personne": Date_naissance_personne}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_genre = """INSERT INTO t_personne (Id_personne,Nom_personne,Prenom_personne,Date_naissance_personne) VALUES (NULL,%(value_nom_personne)s,%(value_prenom_personne)s,%(value_Date_naissance_personne)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_genre, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('genres_afficher', order_by='DESC', id_genre_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{genres_ajouter_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("personnes/personne_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update
    
    Test : ex cliquer sur le menu "personnes" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "personne_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "personnes/personne_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@app.route("/genre_update", methods=['GET', 'POST'])
def genre_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "Id_personne"
    id_genre_update = request.values['id_personne_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "personne_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            nom_personne_update = form_update.nom_personne_update_wtf.data
            nom_personne_update = nom_personne_update.capitalize()

            prenom_personne_update = form_update.prenom_personne_update_wtf.data
            prenom_personne_update = prenom_personne_update.capitalize()


            Date_naissance_personne_essai = form_update.Date_naissance_personne_wtf.data
            Date_naissance_personne_essai = Date_naissance_personne_essai


            valeur_update_dictionnaire = {"value_id_personne": id_genre_update,
                                                  "value_nom_personne": nom_personne_update,
                                                  "value_prenom_personne": prenom_personne_update,
                                                  "value_Date_naissance_personne": Date_naissance_personne_essai}

            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_personne
                                              SET Nom_personne = %(value_nom_personne)s,
                                              Prenom_personne = %(value_prenom_personne)s,
                                              Date_naissance_personne = %(value_Date_naissance_personne)s
                                              WHERE Id_personne = %(value_id_personne)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=id_genre_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "Id_personne" et "Nom_personne" de la "t_personne"
            str_sql_id_genre = "SELECT Id_personne, Nom_personne, Prenom_personne, Date_naissance_personne FROM t_personne WHERE Id_personne = %(value_id_personne)s"
            valeur_select_dictionnaire = {"value_id_personne": id_genre_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_genre = mybd_conn.fetchone()
            print(" ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                  data_nom_genre["Nom_personne"])


            # Afficher la valeur sélectionnée dans les champs du formulaire "personne_update_wtf.html"
            form_update.nom_personne_update_wtf.data = data_nom_genre["Nom_personne"]
            form_update.prenom_personne_update_wtf.data = data_nom_genre["Prenom_personne"]
            form_update.Date_naissance_personne_wtf.data = data_nom_genre["Date_naissance_personne"]

    except Exception as Exception_genre_update_wtf:
        raise ExceptionGenreUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_update_wtf.__name__} ; "
                                      f"{Exception_genre_update_wtf}")

    return render_template("personnes/personne_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete
    
    Test : ex. cliquer sur le menu "personnes" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "personne_afficher.html"
    
    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "personnes/personne_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@app.route("/genre_delete", methods=['GET', 'POST'])
def genre_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "Id_personne"
    id_personne_delete = request.values['id_personne_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteGenre()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("genres_afficher", order_by="ASC", id_genre_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "personnes/personne_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer la personnes de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_genre": id_personne_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_films_genre = """DELETE FROM t_avoir_droit
                                                WHERE FK_personne = %(value_id_genre)s"""
                str_sql_delete_idgenre = """DELETE FROM t_personne
                                            WHERE Id_personne = %(value_id_genre)s"""
                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(str_sql_delete_films_genre, valeur_delete_dictionnaire)
                    mconn_bd.execute(str_sql_delete_idgenre, valeur_delete_dictionnaire)

                flash(f"Personne définitivement effacée !!", "success")
                print(f"Genre définitivement effacé !!")

                # afficher les données
                return redirect(url_for('genres_afficher', order_by="ASC", id_genre_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_genre": id_personne_delete}
            print(id_personne_delete, type(id_personne_delete))

            # Requête qui affiche tous les Avoir_droit qui ont le genre que l'utilisateur veut effacer
            str_sql_genres_films_delete = """SELECT id_droit, droit FROM t_avoir_droit 
                                            INNER JOIN t_droit ON t_avoir_droit.FK_droit = t_droit.id_droit
                                            INNER JOIN t_personne ON t_avoir_droit.FK_personne = t_personne.Id_personne
                                            WHERE FK_personne = %(value_id_genre)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_films_attribue_genre_delete = mydb_conn.fetchall()
                print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "personnes/personne_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

                # Opération sur la BD pour récupérer "Id_personne" et "Nom_personne" de la "t_personne"
                str_sql_id_genre = "SELECT Id_personne, Nom_personne, Prenom_personne, Date_naissance_personne FROM t_personne WHERE Id_personne = %(value_id_genre)s"

                mydb_conn.execute(str_sql_id_genre, valeur_select_dictionnaire)
                # Une seule valeur est suffisante "fetchone()",
                # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
                data_nom_genre = mydb_conn.fetchone()
                print("data_nom_genre ", data_nom_genre, " type ", type(data_nom_genre), " genre ",
                      data_nom_genre["Nom_personne"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "personne_delete_wtf.html"
            form_delete.nom_genre_delete_wtf.data = data_nom_genre["Nom_personne"]
            form_delete.prenom_genre_delete_wtf.data = data_nom_genre["Prenom_personne"]
            form_delete.date_genre_delete_wtf.data = data_nom_genre["Date_naissance_personne"]

            # Le bouton pour l'action "DELETE" dans le form. "personne_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_genre_delete_wtf:
        raise ExceptionGenreDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                      f"{genre_delete_wtf.__name__} ; "
                                      f"{Exception_genre_delete_wtf}")

    return render_template("personnes/personne_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
