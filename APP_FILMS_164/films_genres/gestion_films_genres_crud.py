"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les personne.
"""
from pathlib import Path

from flask import redirect
from flask import request
from flask import session
from flask import url_for

from APP_FILMS_164.database.database_tools import DBconnection
from APP_FILMS_164.erreurs.exceptions import *

"""
    Nom : avoir_droit_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /avoir_droit_afficher
    
    But : Afficher les films avec les personne associés pour chaque adresse.
    
    Paramètres : id_genre_sel = 0 >> tous les films.
                 id_genre_sel = "n" affiche le adresse dont l'id est "n"
                 
"""


@app.route("/droit_afficher/<int:id_personne_sel>", methods=['GET', 'POST'])
def avoir_droit_afficher(id_personne_sel):
    print(" droit_afficher  ", id_personne_sel)
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_avoir_droit_afficher_data = """SELECT Id_personne, Nom_personne, Prenom_personne, Date_naissance_personne,
                                                            GROUP_CONCAT(droit) as AvoirDroit FROM t_avoir_droit
                                                            RIGHT JOIN t_personne ON t_personne.Id_personne = t_avoir_droit.fk_personne
                                                            LEFT JOIN t_droit ON t_droit.id_droit = t_avoir_droit.fk_droit
                                                            GROUP BY Id_personne"""
                if id_personne_sel == 0:
                    # le paramètre 0 permet d'afficher tous les films
                    # Sinon le paramètre représente la valeur de l'id du adresse
                    mc_afficher.execute(strsql_avoir_droit_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du adresse sélectionné avec un nom de variable
                    valeur_id_personne_selected_dictionnaire = {"value_Id_personne_selected": id_personne_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_avoir_droit_afficher_data += """ HAVING Id_personne= %(value_Id_personne_selected)s"""

                    mc_afficher.execute(strsql_avoir_droit_afficher_data, valeur_id_personne_selected_dictionnaire)

                # Récupère les données de la requête.
                data_avoir_droit_afficher = mc_afficher.fetchall()
                print("data_droit ", data_avoir_droit_afficher, " Type : ", type(data_avoir_droit_afficher))

                # Différencier les messages.
                if not data_avoir_droit_afficher and id_personne_sel == 0:
                    flash("""La table "t_personne" est vide. !""", "warning")
                elif not data_avoir_droit_afficher and id_personne_sel > 0:
                    # Si l'utilisateur change l'id_adresse dans l'URL et qu'il ne correspond à aucun adresse
                    flash(f"La personne {id_personne_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données personne et droit affichés !!", "success")

        except Exception as Exception_avoir_droit_afficher:
            raise ExceptionPersonneDroitAfficher(f"fichier : {Path(__file__).name}  ;  {avoir_droit_afficher.__name__} ;"
                                               f"{Exception_avoir_droit_afficher}")

    print("avoir_droit_afficher  ", data_avoir_droit_afficher)
    # Envoie la page "HTML" au serveur.
    return render_template("avoir_droit/avoir_droit_afficher.html", data=data_avoir_droit_afficher)


"""
    nom: edit_avoir_droit_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les personne du adresse sélectionné par le bouton "MODIFIER" de "avoir_droit_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les personne contenus dans la "t_personne".
    2) Les personne attribués au adresse selectionné.
    3) Les personne non-attribués au personne sélectionné.

    On signale les erreurs importantes

"""


@app.route("/edit_avoir_droit_selected", methods=['GET', 'POST'])
def edit_avoir_droit_selected():
    if request.method == "GET":
        try:
            with DBconnection() as mc_afficher:
                strsql_droit_afficher = """SELECT Id_personne, nom_personne droit FROM t_personne WHERE Id_personne ASC"""
                mc_afficher.execute(strsql_droit_afficher)
            data_droit_all = mc_afficher.fetchall()
            print("dans edit_avoir_droit_selected ---> data_droit_all", data_droit_all)

            # Récupère la valeur de "id_adresse" du formulaire html "avoir_droit_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_adresse"
            # grâce à la variable "id_film_genres_edit_html" dans le fichier "avoir_droit_afficher.html"
            # href="{{ url_for('edit_avoir_droit_selected', id_film_genres_edit_html=row.id_adresse) }}"
            id_avoir_droit_edit = request.values['id_avoir_personne_edit_html']

            # Mémorise l'id du adresse dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_avoir_droit_edit'] = id_avoir_droit_edit

            # Constitution d'un dictionnaire pour associer l'id du adresse sélectionné avec un nom de variable
            valeur_id_personne_selected_dictionnaire = {"value_Id_personne_selected": id_avoir_droit_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction avoir_droit_afficher_data
            # 1) Sélection du adresse choisi
            # 2) Sélection des personne "déjà" attribués pour le adresse.
            # 3) Sélection des personne "pas encore" attribués pour le adresse choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "avoir_droit_afficher_data"
            data_avoir_droit_selected, data_avoir_droit_non_attribues, data_avoir_droit_attribues = \
                avoir_droit_afficher_data(valeur_id_personne_selected_dictionnaire)

            print(data_avoir_droit_selected)
            lst_data_personne_selected = [item['Id_personne'] for item in data_avoir_droit_selected]
            print("lst_data_personne_selected  ", lst_data_personne_selected,
                  type(lst_data_personne_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les personne qui ne sont pas encore sélectionnés.
            lst_data_avoir_droit_non_attribues = [item['id_droit'] for item in data_avoir_droit_non_attribues]
            session['session_lst_data_avoir_droit_non_attribues'] = lst_data_avoir_droit_non_attribues
            print("lst_data_avoir_droit_non_attribues  ", lst_data_avoir_droit_non_attribues,
                  type(lst_data_avoir_droit_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les personne qui sont déjà sélectionnés.
            lst_data_avoir_droit_old_attribues = [item['id_personne'] for item in data_avoir_droit_attribues]
            session['session_lst_data_avoir_droit_old_attribues'] = lst_data_avoir_droit_old_attribues
            print("lst_data_avoir_droit_old_attribues  ", lst_data_avoir_droit_old_attribues,
                  type(lst_data_avoir_droit_old_attribues))

            print(" data data_avoir_droit_selected", data_avoir_droit_selected, "type ", type(data_avoir_droit_selected))
            print(" data data_avoir_droit_non_attribues ", data_avoir_droit_non_attribues, "type ",
                  type(data_avoir_droit_non_attribues))
            print(" data_avoir_droit_attribues ", data_avoir_droit_attribues, "type ",
                  type(data_avoir_droit_attribues))

            # Extrait les valeurs contenues dans la table "t_genres", colonne "Nom_personne"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'Id_personne
            lst_data_avoir_droit_non_attribues = [item['droit'] for item in data_avoir_droit_non_attribues]
            print("lst_all_droit gf_edit_avoir_droit_selected ", lst_data_avoir_droit_non_attribues,
                  type(lst_data_avoir_droit_non_attribues))

        except Exception as Exception_edit_avoir_droit_selected:
            raise ExceptionEditDroitPersonneSelected(f"fichier : {Path(__file__).name}  ;  "
                                                 f"{edit_avoir_droit_selected.__name__} ; "
                                                 f"{Exception_edit_avoir_droit_selected}")

    return render_template("Avoir_droit/films_genres_modifier_tags_dropbox.html",
                           data_droit=data_droit_all,
                           data_personne_selected=data_avoir_droit_selected,
                           data_droit_attribues=data_avoir_droit_attribues,
                           data_droit_non_attribues=data_avoir_droit_non_attribues)


"""
    nom: update_avoir_droit_selected

    Récupère la liste de tous les personne du adresse sélectionné par le bouton "MODIFIER" de "avoir_droit_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les personne contenus dans la "t_droit".
    2) Les personne attribués au adresse selectionné.
    3) Les personne non-attribués au adresse sélectionné.

    On signale les erreurs importantes
"""


@app.route("/update_avoir_droit_selected", methods=['GET', 'POST'])
def update_avoir_droit_selected():
    if request.method == "POST":
        try:
            # Récupère l'id du adresse sélectionné
            id_personne_selected = session['session_id_avoir_droit_edit']
            print("session['session_id_avoir_droit_edit'] ", session['session_id_avoir_droit_edit'])

            # Récupère la liste des personne qui ne sont pas associés au adresse sélectionné.
            old_lst_data_avoir_droit_non_attribues = session['session_lst_data_avoir_droit_non_attribues']
            print("old_lst_data_avoir_droit_non_attribues ", old_lst_data_avoir_droit_non_attribues)

            # Récupère la liste des personne qui sont associés au adresse sélectionné.
            old_lst_data_avoir_droit_attribues = session['session_lst_avoir_droit_films_old_attribues']
            print("old_lst_avoir_droit_films_old_attribues ", old_lst_data_avoir_droit_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme personne dans le composant "tags-selector-tagselect"
            # dans le fichier "genres_films_modifier_tags_dropbox.html"
            new_lst_str_avoir_droit = request.form.getlist('name_select_tags')
            print("new_lst_str_avoir_droit ", new_lst_str_avoir_droit)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_avoir_droit_old = list(map(int, new_lst_str_avoir_droit))
            print("new_lst_avoir_droit ", new_lst_int_avoir_droit_old, "type new_lst_avoir_droit ",
                  type(new_lst_int_avoir_droit_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "Id_personne" qui doivent être effacés de la table intermédiaire "t_genre_film".
            lst_diff_genres_delete_b = list(set(old_lst_data_avoir_droit_attribues) -
                                            set(new_lst_int_avoir_droit_old))
            print("lst_diff_droit_delete_b ", lst_diff_genres_delete_b)

            # Une liste de "Id_personne" qui doivent être ajoutés à la "t_genre_film"
            lst_diff_droit_insert_a = list(
                set(new_lst_int_avoir_droit_old) - set(old_lst_data_avoir_droit_attribues))
            print("lst_diff_droit_insert_a ", lst_diff_droit_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_film"/"id_adresse" et "fk_genre"/"Id_personne" dans la "t_genre_film"
            strsql_insert_avoir_droit = """INSERT INTO t_avoir_droit (id_avoir_droit, fk_personne, fk_droit)
                                                    VALUES (NULL, %(value_fk_personne)s, %(value_fk_droit)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_adresse" et "Id_personne" dans la "t_genre_film"
            strsql_delete_avoir_droit = """DELETE FROM t_avoir_droit WHERE fk_droit = %(value_fk_droit)s AND fk_personne = %(value_fk_personne)s"""

            with DBconnection() as mconn_bd:
                # Pour le adresse sélectionné, parcourir la liste des personne à INSÉRER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_droit_ins in lst_diff_droit_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du adresse sélectionné avec un nom de variable
                    # et "id_genre_ins" (l'id du genre dans la liste) associé à une variable.
                    valeurs_personne_sel_droit_sel_dictionnaire = {"value_fk_personne": id_personne_selected,
                                                               "value_fk_droit": id_droit_ins}

                    mconn_bd.execute(strsql_insert_avoir_droit, valeurs_personne_sel_droit_sel_dictionnaire)

                # Pour le adresse sélectionné, parcourir la liste des personne à EFFACER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_droit_del in lst_diff_genres_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du adresse sélectionné avec un nom de variable
                    # et "id_genre_del" (l'id du genre dans la liste) associé à une variable.
                    valeurs_film_sel_genre_sel_dictionnaire = {"value_fk_personne": id_personne_selected,
                                                               "value_fk_droit": id_droit_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "execute" dans la classe "DBconnection"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "DBconnection"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.execute(strsql_delete_avoir_droit, valeurs_film_sel_genre_sel_dictionnaire)

        except Exception as Exception_update_avoir_droit_selected:
            raise ExceptionUpdateGenreFilmSelected(f"fichier : {Path(__file__).name}  ;  "
                                                   f"{update_avoir_droit_selected.__name__} ; "
                                                   f"{Exception_update_avoir_droit_selected}")

    # Après cette mise à jour de la table intermédiaire "t_genre_film",
    # on affiche les films et le(urs) genre(s) associé(s).
    return redirect(url_for('droit_afficher', id_personne_sel=id_personne_selected))


"""
    nom: avoir_droit_afficher_data

    Récupère la liste de tous les personne du adresse sélectionné par le bouton "MODIFIER" de "avoir_droit_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des personne, ainsi l'utilisateur voit les personne à disposition

    On signale les erreurs importantes
"""


def avoir_droit_afficher_data(valeur_id_personne_selected_dict):
    print("valeur_id_personne_selected_dict...", valeur_id_personne_selected_dict)
    try:

        strsql_personne_selected = """SELECT Id_personne, nom_personne, Prenom_personne, Date_naisannce_personne, GROUP_CONCAT(id_droit) as AvoirDroit FROM t_avoir_droit
                                        INNER JOIN t_personne ON t_personne.Id_personne = t_avoir_droit.Fk_personne
                                        INNER JOIN t_droit ON t_droit.id_droit = t_avoir_droit.Fk_droit
                                        WHERE Id_personne = %(value_Id_personne_selected)s"""

        strsql_avoir_droit_non_attribues = """SELECT id_droit, droit FROM t_droit WHERE id_droit not in(SELECT Id_personne as idAvoirDroit FROM t_avoir_droit
                                                    INNER JOIN t_personne ON t_personne.Id_personne = t_avoir_droit.Fk_personne
                                                    INNER JOIN t_droit ON t_droit.id_droit = t_avoir_droit.fk_droit
                                                    WHERE Id_personne = %(value_Id_personne_selected)s)"""

        strsql_avoir_droit_attribues = """SELECT Id_personne, id_droit, droit FROM t_avoir_droit
                                            INNER JOIN t_personne ON t_personne.Id_perssonne = t_avoir_droit.Fk_personne
                                            INNER JOIN t_droit ON t_droit.id_droit = t_avoir_droit.Fk_droit
                                            WHERE Id_personne = %(value_Id_personne_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with DBconnection() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_avoir_droit_non_attribues, valeur_id_personne_selected_dict)
            # Récupère les données de la requête.
            data_avoir_droit_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("avoir_droit_afficher_data ----> data_avoir_droit_non_attribues ", data_avoir_droit_non_attribues,
                  " Type : ",
                  type(data_avoir_droit_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_personne_selected, valeur_id_personne_selected_dict)
            # Récupère les données de la requête.
            data_film_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_personne_selected  ", data_film_selected, " Type : ", type(data_film_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_avoir_droit_attribues, valeur_id_personne_selected_dict)
            # Récupère les données de la requête.
            data_avoir_droit_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_avoir_droit_attribues ", data_avoir_droit_attribues, " Type : ",
                  type(data_avoir_droit_attribues))

            # Retourne les données des "SELECT"
            return data_film_selected, data_avoir_droit_non_attribues, data_avoir_droit_attribues

    except Exception as Exception_avoir_droit_afficher_data:
        raise ExceptionAvoirDroitAfficherData(f"fichier : {Path(__file__).name}  ;  "
                                               f"{avoir_droit_afficher_data.__name__} ; "
                                               f"{Exception_avoir_droit_afficher_data}")
