-- OM 2021.02.17
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: zzz_xxxxx_NOM_PRENOM_INFO1X_SUJET_104_2021

-- Détection si une autre base de donnée du même nom existe

DROP DATABASE IF EXISTS andrea_pelliccione_info1b_gestion_appartement;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS andrea_pelliccione_info1b_gestion_appartement;

-- Utilisation de cette base de donnée

USE andrea_pelliccione_info1b_gestion_appartement;
-- --------------------------------------------------------

--
--
-- Base de données :  `andrea_pelliccione_info1b_gestion_appartement`
--

-- --------------------------------------------------------

--
-- Structure de la table `t_adresse`
--

CREATE TABLE `t_adresse` (
  `id_adresse` int(25) NOT NULL,
  `pays` varchar(20) NOT NULL,
  `npa` varchar(20) NOT NULL,
  `ville` varchar(20) NOT NULL,
  `rue` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_adresse`
--

INSERT INTO `t_adresse` (`id_adresse`, `pays`, `npa`, `ville`, `rue`) VALUES
(1, 'Suisse', '1020', 'Renens', 'Ch. du Bugnon 43'),
(2, 'Suisse', '1623', 'Semsales', 'Le Pra-Roud 15'),
(3, 'Suisse', '1032', 'Romanel', 'Ch. de la courtois 3'),
(4, 'Suisse', '1033', 'Crissier', 'La praronde 43'),
(5, 'Suisse', '1057', 'La salah', 'Rue de la coline 2'),
(6, 'Suisse', '1098', 'Zurich', 'Rue de la strasse 67'),
(7, 'Suisse', '1054', 'Renens', 'Rue du lac 72'),
(8, 'Suisse', '1078', 'Bâle', 'Rue de la grae 08');

-- --------------------------------------------------------

--
-- Structure de la table `t_appartement`
--

CREATE TABLE `t_appartement` (
  `Id_appartement` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_appartement`
--

INSERT INTO `t_appartement` (`Id_appartement`) VALUES
(1);

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_droit`
--

CREATE TABLE `t_avoir_droit` (
  `id_avoir_droit` int(11) NOT NULL,
  `Fk_personne` int(11) NOT NULL,
  `Fk_droit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_avoir_droit`
--

INSERT INTO `t_avoir_droit` (`id_avoir_droit`, `Fk_personne`, `Fk_droit`) VALUES
(1, 1, 2),
(2, 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_lit`
--

CREATE TABLE `t_avoir_lit` (
  `Id_avoir_lit` int(11) NOT NULL,
  `Fk_piece` int(11) NOT NULL,
  `Fk_lit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_avoir_lit`
--

INSERT INTO `t_avoir_lit` (`Id_avoir_lit`, `Fk_piece`, `Fk_lit`) VALUES
(1, 1, 1),
(2, 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `t_contenu`
--

CREATE TABLE `t_contenu` (
  `Id_contenu` int(11) NOT NULL,
  `fk_piece` int(11) DEFAULT NULL,
  `contenu` varchar(50) NOT NULL,
  `Nb_contenu` int(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_contenu`
--

INSERT INTO `t_contenu` (`Id_contenu`, `fk_piece`, `contenu`, `Nb_contenu`) VALUES
(7, 4, 'asdfaaaaaaa', 15),
(9, 4, 'sadfdsa', 189);

-- --------------------------------------------------------

--
-- Structure de la table `t_droit`
--

CREATE TABLE `t_droit` (
  `id_droit` int(11) NOT NULL,
  `droit` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_droit`
--

INSERT INTO `t_droit` (`id_droit`, `droit`) VALUES
(1, 'User'),
(2, 'admin'),
(3, 'Développeur'),
(4, 'Locataire');

-- --------------------------------------------------------

--
-- Structure de la table `t_etat_lit`
--

CREATE TABLE `t_etat_lit` (
  `Id_etat_lit` int(11) NOT NULL,
  `Etat_lit` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_etat_lit`
--

INSERT INTO `t_etat_lit` (`Id_etat_lit`, `Etat_lit`) VALUES
(1, 'Fait'),
(2, 'Pas fait');

-- --------------------------------------------------------

--
-- Structure de la table `t_lit`
--

CREATE TABLE `t_lit` (
  `Id_lit` int(11) NOT NULL,
  `Fk_type_lit` int(11) NOT NULL,
  `Fk_etat_lit` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_lit`
--

INSERT INTO `t_lit` (`Id_lit`, `Fk_type_lit`, `Fk_etat_lit`) VALUES
(1, 1, 1),
(2, 2, 2);

-- --------------------------------------------------------

--
-- Structure de la table `t_personne`
--

CREATE TABLE `t_personne` (
  `Id_personne` int(11) NOT NULL,
  `Nom_personne` varchar(50) NOT NULL,
  `Prenom_personne` varchar(50) NOT NULL,
  `Date_naissance_personne` date DEFAULT NULL,
  `Adresse_mail_personne` varchar(100) NOT NULL,
  `MDP_personne` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_personne`
--

INSERT INTO `t_personne` (`Id_personne`, `Nom_personne`, `Prenom_personne`, `Date_naissance_personne`, `Adresse_mail_personne`, `MDP_personne`) VALUES
(1, 'pelliccione', 'andrea', '2005-03-08', 'andrea.pelliccione@gmail.com', '*79A8858EDF279DC3B99BA41350FE3CF1ABEFC655'),
(2, 'Steiner', 'Theo', '2005-09-04', 'steiner.theo@gmail.com', '01234'),
(3, 'Boescher', 'Fyn', '2004-04-04', 'boescher.fyn@bluewin.ch', '14540'),
(4, 'gerard', 'depard', '2002-03-06', 'gerard.depard@outlook.com', '548731'),
(5, 'kanlo ', 'brebis', '2001-07-13', 'kanlo.brebis@yahoo.com', '861826'),
(6, 'paddle', 'blanco', '1996-08-23', 'paddle.blanco@gmail.com', '755462'),
(7, 'picolo', 'bernardo', '1990-02-07', 'picolo.bernardo@bluewin.ch', '76565956'),
(8, 'bonadelo', 'pascal', '1972-10-13', 'bonadelo.pascal@outlook.ch', '987456');

-- --------------------------------------------------------

--
-- Structure de la table `t_personne_avoir_adresse`
--

CREATE TABLE `t_personne_avoir_adresse` (
  `id_personne_adresse` int(34) NOT NULL,
  `Date_adresse` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fk_personne` int(11) DEFAULT NULL,
  `fk_adresse` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_personne_avoir_adresse`
--

INSERT INTO `t_personne_avoir_adresse` (`id_personne_adresse`, `Date_adresse`, `fk_personne`, `fk_adresse`) VALUES
(1, '2022-05-18 11:19:46', 1, 3),
(2, '2022-05-18 11:19:46', 2, 7),
(3, '2022-05-18 11:26:47', 3, 5),
(4, '2022-05-18 11:26:47', 4, 6),
(5, '2022-05-18 11:27:36', 5, 4),
(6, '2022-05-18 11:27:36', 7, 8);

-- --------------------------------------------------------

--
-- Structure de la table `t_piece`
--

CREATE TABLE `t_piece` (
  `Id_piece` int(11) NOT NULL,
  `Fk_appartement` int(11) NOT NULL,
  `Nom_piece` varchar(50) NOT NULL,
  `Surface_piece` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_piece`
--

INSERT INTO `t_piece` (`Id_piece`, `Fk_appartement`, `Nom_piece`, `Surface_piece`) VALUES
(1, 1, 'Chambre 1', 12),
(2, 1, 'Cuisine', 42),
(4, 1, 'salon', 34);

-- --------------------------------------------------------

--
-- Structure de la table `t_reservations`
--

CREATE TABLE `t_reservations` (
  `Id_reservations` int(11) NOT NULL,
  `Fk_personne` int(11) NOT NULL,
  `Fk_appartement` int(11) NOT NULL,
  `Date_reservations` date NOT NULL,
  `Nombre_personne` int(11) NOT NULL,
  `Nombre_jour_reservations` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_reservations`
--

INSERT INTO `t_reservations` (`Id_reservations`, `Fk_personne`, `Fk_appartement`, `Date_reservations`, `Nombre_personne`, `Nombre_jour_reservations`) VALUES
(1, 1, 1, '2021-04-02', 5, 2);

-- --------------------------------------------------------

--
-- Structure de la table `t_type_lit`
--

CREATE TABLE `t_type_lit` (
  `Id_type_lit` int(11) NOT NULL,
  `Type_lit` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Contenu de la table `t_type_lit`
--

INSERT INTO `t_type_lit` (`Id_type_lit`, `Type_lit`) VALUES
(1, 'Lit simple'),
(2, 'Lit double'),
(3, 'lit superposer');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `t_adresse`
--
ALTER TABLE `t_adresse`
  ADD PRIMARY KEY (`id_adresse`);

--
-- Index pour la table `t_appartement`
--
ALTER TABLE `t_appartement`
  ADD PRIMARY KEY (`Id_appartement`);

--
-- Index pour la table `t_avoir_droit`
--
ALTER TABLE `t_avoir_droit`
  ADD PRIMARY KEY (`id_avoir_droit`),
  ADD KEY `Fk_personne` (`Fk_personne`),
  ADD KEY `Fk_droit` (`Fk_droit`);

--
-- Index pour la table `t_avoir_lit`
--
ALTER TABLE `t_avoir_lit`
  ADD PRIMARY KEY (`Id_avoir_lit`),
  ADD KEY `Fk_piece` (`Fk_piece`,`Fk_lit`),
  ADD KEY `Fk_lit` (`Fk_lit`);

--
-- Index pour la table `t_contenu`
--
ALTER TABLE `t_contenu`
  ADD PRIMARY KEY (`Id_contenu`),
  ADD KEY `id_piece` (`fk_piece`);

--
-- Index pour la table `t_droit`
--
ALTER TABLE `t_droit`
  ADD PRIMARY KEY (`id_droit`);

--
-- Index pour la table `t_etat_lit`
--
ALTER TABLE `t_etat_lit`
  ADD PRIMARY KEY (`Id_etat_lit`);

--
-- Index pour la table `t_lit`
--
ALTER TABLE `t_lit`
  ADD PRIMARY KEY (`Id_lit`),
  ADD KEY `Fk_etat_lit` (`Fk_etat_lit`),
  ADD KEY `Fk_type_lit` (`Fk_type_lit`);

--
-- Index pour la table `t_personne`
--
ALTER TABLE `t_personne`
  ADD PRIMARY KEY (`Id_personne`);

--
-- Index pour la table `t_personne_avoir_adresse`
--
ALTER TABLE `t_personne_avoir_adresse`
  ADD PRIMARY KEY (`id_personne_adresse`),
  ADD KEY `fk_personne` (`fk_personne`),
  ADD KEY `fk_adresse` (`fk_adresse`);

--
-- Index pour la table `t_piece`
--
ALTER TABLE `t_piece`
  ADD PRIMARY KEY (`Id_piece`),
  ADD KEY `Fk_appartement` (`Fk_appartement`);

--
-- Index pour la table `t_reservations`
--
ALTER TABLE `t_reservations`
  ADD PRIMARY KEY (`Id_reservations`),
  ADD KEY `Fk_personne` (`Fk_personne`),
  ADD KEY `Fk_appartement` (`Fk_appartement`);

--
-- Index pour la table `t_type_lit`
--
ALTER TABLE `t_type_lit`
  ADD PRIMARY KEY (`Id_type_lit`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_adresse`
--
ALTER TABLE `t_adresse`
  MODIFY `id_adresse` int(25) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT pour la table `t_appartement`
--
ALTER TABLE `t_appartement`
  MODIFY `Id_appartement` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `t_avoir_droit`
--
ALTER TABLE `t_avoir_droit`
  MODIFY `id_avoir_droit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_avoir_lit`
--
ALTER TABLE `t_avoir_lit`
  MODIFY `Id_avoir_lit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_contenu`
--
ALTER TABLE `t_contenu`
  MODIFY `Id_contenu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT pour la table `t_droit`
--
ALTER TABLE `t_droit`
  MODIFY `id_droit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT pour la table `t_etat_lit`
--
ALTER TABLE `t_etat_lit`
  MODIFY `Id_etat_lit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_lit`
--
ALTER TABLE `t_lit`
  MODIFY `Id_lit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT pour la table `t_personne`
--
ALTER TABLE `t_personne`
  MODIFY `Id_personne` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
--
-- AUTO_INCREMENT pour la table `t_personne_avoir_adresse`
--
ALTER TABLE `t_personne_avoir_adresse`
  MODIFY `id_personne_adresse` int(34) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT pour la table `t_piece`
--
ALTER TABLE `t_piece`
  MODIFY `Id_piece` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT pour la table `t_reservations`
--
ALTER TABLE `t_reservations`
  MODIFY `Id_reservations` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT pour la table `t_type_lit`
--
ALTER TABLE `t_type_lit`
  MODIFY `Id_type_lit` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `t_avoir_droit`
--
ALTER TABLE `t_avoir_droit`
  ADD CONSTRAINT `t_avoir_droit_ibfk_1` FOREIGN KEY (`Fk_personne`) REFERENCES `t_personne` (`Id_personne`),
  ADD CONSTRAINT `t_avoir_droit_ibfk_2` FOREIGN KEY (`Fk_droit`) REFERENCES `t_droit` (`id_droit`);

--
-- Contraintes pour la table `t_avoir_lit`
--
ALTER TABLE `t_avoir_lit`
  ADD CONSTRAINT `t_avoir_lit_ibfk_1` FOREIGN KEY (`Fk_lit`) REFERENCES `t_lit` (`Id_lit`),
  ADD CONSTRAINT `t_avoir_lit_ibfk_2` FOREIGN KEY (`Fk_piece`) REFERENCES `t_piece` (`Id_piece`);

--
-- Contraintes pour la table `t_contenu`
--
ALTER TABLE `t_contenu`
  ADD CONSTRAINT `t_contenu_ibfk_1` FOREIGN KEY (`fk_piece`) REFERENCES `t_piece` (`Id_piece`) ON DELETE SET NULL ON UPDATE SET NULL;

--
-- Contraintes pour la table `t_lit`
--
ALTER TABLE `t_lit`
  ADD CONSTRAINT `t_lit_ibfk_1` FOREIGN KEY (`Fk_etat_lit`) REFERENCES `t_etat_lit` (`Id_etat_lit`),
  ADD CONSTRAINT `t_lit_ibfk_2` FOREIGN KEY (`Fk_type_lit`) REFERENCES `t_type_lit` (`Id_type_lit`);

--
-- Contraintes pour la table `t_personne_avoir_adresse`
--
ALTER TABLE `t_personne_avoir_adresse`
  ADD CONSTRAINT `fk_pers_adresse_pers` FOREIGN KEY (`fk_adresse`) REFERENCES `t_adresse` (`id_adresse`),
  ADD CONSTRAINT `fk_pers_pers_addresse` FOREIGN KEY (`fk_personne`) REFERENCES `t_personne` (`Id_personne`);

--
-- Contraintes pour la table `t_piece`
--
ALTER TABLE `t_piece`
  ADD CONSTRAINT `t_piece_ibfk_1` FOREIGN KEY (`Fk_appartement`) REFERENCES `t_appartement` (`Id_appartement`);

--
-- Contraintes pour la table `t_reservations`
--
ALTER TABLE `t_reservations`
  ADD CONSTRAINT `t_reservations_ibfk_1` FOREIGN KEY (`Fk_personne`) REFERENCES `t_personne` (`Id_personne`),
  ADD CONSTRAINT `t_reservations_ibfk_2` FOREIGN KEY (`Fk_appartement`) REFERENCES `t_appartement` (`Id_appartement`);
