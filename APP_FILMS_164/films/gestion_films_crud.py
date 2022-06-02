"""Gestion des "routes" FLASK et des données pour les films.
Fichier : gestion_films_crud.py
Auteur : OM 2022.04.11
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *
from APP_FILMS_164.films.gestion_films_wtf_forms import FormWTFAddFilm
from APP_FILMS_164.films.gestion_films_wtf_forms import FormWTFUpdateFilm
from APP_FILMS_164.films.gestion_films_wtf_forms import FormWTFDeleteFilm

"""Ajouter un droit grâce au formulaire "film_add_wtf.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_add

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "ADD" d'un "droit"

Paramètres : sans


Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python dans le fichier ""
            On ne doit pas accepter un champ vide.
"""

@app.route("/droit_afficher/<string:order_by>/<int:id_details_sel>", methods=['GET', 'POST'])
def droit_afficher(order_by, id_details_sel):
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                if order_by == "ASC" and id_details_sel == 0:
                    strsql_droit_afficher = """SELECT id_droit, droit FROM t_droit ORDER BY id_droit ASC"""
                    mc_afficher.execute(strsql_droit_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_personne"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_genre_selected_dictionnaire = {"value_id_genre_selected": id_details_sel}
                    strsql_droit_afficher = """SELECT id_droit, droit FROM t_droit WHERE id_droit = %(value_id_genre_selected)s"""

                    mc_afficher.execute(strsql_droit_afficher, valeur_id_genre_selected_dictionnaire)
                else:
                    strsql_droit_afficher = """SELECT id_droit, droit FROM t_droit ORDER BY id_droit DESC"""

                    mc_afficher.execute(strsql_droit_afficher)

                data_genres = mc_afficher.fetchall()

                print("data_genres ", data_genres, " Type : ", type(data_genres))

                # Différencier les messages si la table est vide.
                if not data_genres and id_details_sel == 0:
                    flash("""La table "t_personne" est vide. !!""", "warning")
                elif not data_genres and id_details_sel > 0:
                    # Si l'utilisateur change l'Id_personne dans l'URL et que le genre n'existe pas,
                    flash(f"Le personne demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_personne" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données droit affichés !!", "success")

        except Exception as Exception_genres_afficher:
            raise ExceptionGenresAfficher(f"fichier : {Path(__file__).name}  ;  "
                                          f"{droit_afficher.__name__} ; "
                                          f"{Exception_genres_afficher}")

    # Envoie la page "HTML" au serveur.
    return render_template("films/films_afficher.html", data=data_genres)


@app.route("/film_add", methods=['GET', 'POST'])
def film_add_wtf():
    # Objet formulaire pour AJOUTER un droit
    form_add_film = FormWTFAddFilm()
    if request.method == "POST":
        try:
            if form_add_film.validate_on_submit():
                nom_film_add = form_add_film.nom_film_add_wtf.data

                valeurs_insertion_dictionnaire = {"value_nom_film": nom_film_add}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_droit = """INSERT INTO t_droit (id_droit,droit) VALUES (NULL,%(value_nom_film)s) """
                with DBconnection() as mconn_bd:
                    mconn_bd.execute(strsql_insert_droit, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion du nouveau droit (id_personne_sel=0 => afficher tous les films)
                return redirect(url_for('droit_afficher', order_by='DESC', id_details_sel=0))

        except Exception as Exception_genres_ajouter_wtf:
            raise ExceptionGenresAjouterWtf(f"fichier : {Path(__file__).name}  ;  "
                                            f"{film_add_wtf.__name__} ; "
                                            f"{Exception_genres_ajouter_wtf}")

    return render_template("films/film_add_wtf.html", form_add_film=form_add_film)


"""Editer(update) un droit qui a été sélectionné dans le formulaire "avoir_droit_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_update

Test : exemple: cliquer sur le menu "Films/Genres" puis cliquer sur le bouton "EDIT" d'un "droit"

Paramètres : sans

But : Editer(update) un genre qui a été sélectionné dans le formulaire "personne_afficher.html"

Remarque :  Dans le champ "nom_film_update_wtf" du formulaire "films/films_update_wtf.html",
            le contrôle de la saisie s'effectue ici en Python.
            On ne doit pas accepter un champ vide.
"""


@app.route("/film_update", methods=['GET', 'POST'])
def film_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_droit"
    id_droit_update = request.values['id_droit_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update_film = FormWTFUpdateFilm()
    try:
        print(" on submit ", form_update_film.validate_on_submit())
        if form_update_film.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            droit_update = form_update_film.nom_film_update_wtf.data
            droit_update = droit_update.capitalize()


            valeur_update_dictionnaire = {"value_id_droit": int(id_droit_update),
                                          "value_droit": droit_update}

            print("valeur_update_dictionnaire ", id_droit_update, droit_update)

            str_sql_update_nom_film = """UPDATE t_droit
                                         SET droit = %(value_droit)s
                                         WHERE id_droit = %(value_id_droit)s """
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_update_nom_film, valeur_update_dictionnaire)


            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Afficher seulement le droit modifié, "ASC" et l'"id_droit_update"
            return redirect(url_for('droit_afficher', order_by='DESC', id_details_sel=id_droit_update))

        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_droit" et "Nom_personne" de la "t_personne"
            str_sql_id_droit = "SELECT id_droit, droit FROM t_droit WHERE id_droit = %(value_id_droit)s"
            valeur_select_dictionnaire = {"value_id_droit": id_droit_update}
            with DBconnection() as mybd_conn:
                mybd_conn.execute(str_sql_id_droit, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_film = mybd_conn.fetchone()

            print("data_film ", data_film, " type ", type(data_film), " genre ",data_film["droit"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "film_update_wtf.html"
            form_update_film.nom_film_update_wtf.data = data_film["droit"]

            # Debug simple pour contrôler la valeur dans la console "run" de PyCharm
            #print(f" duree_film  ", data_film["duree_film"], "  type ", type(data_film["duree_film"]))


    except Exception as Exception_film_update_wtf:
        raise ExceptionFilmUpdateWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{film_update_wtf.__name__} ; "
                                     f"{Exception_film_update_wtf}")

    return render_template("films/film_update_wtf.html", form_update_film=form_update_film)


"""Effacer(delete) un droit qui a été sélectionné dans le formulaire "avoir_droit_afficher.html"
Auteur : OM 2022.04.11
Définition d'une "route" /film_delete
    
Test : ex. cliquer sur le menu "droit" puis cliquer sur le bouton "DELETE" d'un "droit"
    
Paramètres : sans

Remarque :  Dans le champ "nom_film_delete_wtf" du formulaire "films/film_delete_wtf.html"
            On doit simplement cliquer sur "DELETE"
"""


@app.route("/film_delete", methods=['GET', 'POST'])
def film_delete_wtf():
    # Pour afficher ou cacher les boutons "EFFACER"
    data_film_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_droit"
    id_droit_delete = request.values['id_droit_btn_delete_html']

    # Objet formulaire pour effacer le droit sélectionné.
    form_delete_film = FormWTFDeleteFilm()
    try:
        # Si on clique sur "ANNULER", afficher tous les films.
        if form_delete_film.submit_btn_annuler.data:
            return redirect(url_for('droit_afficher', order_by='ASC', id_details_sel=0))

        if form_delete_film.submit_btn_conf_del_film.data:
            # Récupère les données afin d'afficher à nouveau
            # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            data_film_delete = session['data_film_delete']
            print("data_film_delete ", data_film_delete)

            flash(f"Effacer le droit de façon définitive de la BD !!!", "danger")
            # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
            # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
            btn_submit_del = True

        # L'utilisateur a vraiment décidé d'effacer.
        if form_delete_film.submit_btn_del_film.data:
            valeur_delete_dictionnaire = {"value_id_droit": id_droit_delete}
            print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

            str_sql_delete_fk_film_genre = """DELETE FROM t_avoir_droit WHERE FK_droit = %(value_id_droit)s"""
            str_sql_delete_film = """DELETE FROM t_droit WHERE id_droit = %(value_id_droit)s"""
            # Manière brutale d'effacer d'abord la "fk_film", même si elle n'existe pas dans la "t_genre_film"
            # Ensuite on peut effacer le droit vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
            with DBconnection() as mconn_bd:
                mconn_bd.execute(str_sql_delete_fk_film_genre, valeur_delete_dictionnaire)
                mconn_bd.execute(str_sql_delete_film, valeur_delete_dictionnaire)

            flash(f"droit définitivement effacé !!", "success")
            print(f"droit définitivement effacé !!")

            # afficher les données
            return redirect(url_for('droit_afficher', order_by='ASC', id_details_sel=0))
        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_droit": id_droit_delete}
            print(id_droit_delete, type(id_droit_delete))

            # Requête qui affiche le droit qui doit être efffacé.
            str_sql_genres_films_delete = """SELECT * FROM t_droit WHERE id_droit = %(value_id_droit)s"""

            with DBconnection() as mydb_conn:
                mydb_conn.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
                data_film_delete = mydb_conn.fetchall()
                print("data_film_delete...", data_film_delete)

                # Nécessaire pour mémoriser les données afin d'afficher à nouveau
                # le formulaire "films/film_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                session['data_film_delete'] = data_film_delete

            # Le bouton pour l'action "DELETE" dans le form. "film_delete_wtf.html" est caché.
            btn_submit_del = False

    except Exception as Exception_film_delete_wtf:
        raise ExceptionFilmDeleteWtf(f"fichier : {Path(__file__).name}  ;  "
                                     f"{film_delete_wtf.__name__} ; "
                                     f"{Exception_film_delete_wtf}")

    return render_template("films/film_delete_wtf.html",
                           form_delete_film=form_delete_film,
                           btn_submit_del=btn_submit_del,
                           data_film_del=data_film_delete
                           )
