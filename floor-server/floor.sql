-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : db
-- Généré le : sam. 21 jan. 2023 à 01:18
-- Version du serveur : 10.10.2-MariaDB-1:10.10.2+maria~ubu2204
-- Version de PHP : 8.0.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `floor`
--

-- --------------------------------------------------------

--
-- Structure de la table `door permissions`
--

CREATE TABLE `door permissions` (
  `door id` int(11) NOT NULL,
  `permission id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `door permissions`
--

INSERT INTO `door permissions` (`door id`, `permission id`) VALUES
(1, 4),
(2, 3);

-- --------------------------------------------------------

--
-- Structure de la table `doors`
--

CREATE TABLE `doors` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `doors`
--

INSERT INTO `doors` (`id`, `name`) VALUES
(1, 'Conference room'),
(2, 'Janitor closet');

-- --------------------------------------------------------

--
-- Structure de la table `permissions`
--

CREATE TABLE `permissions` (
  `id` int(11) NOT NULL,
  `type` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `permissions`
--

INSERT INTO `permissions` (`id`, `type`) VALUES
(2, 'EMPLOYEE'),
(3, 'VISITOR'),
(4, 'MANAGER'),
(5, 'ADMIN');

-- --------------------------------------------------------

--
-- Structure de la table `user permissions`
--

CREATE TABLE `user permissions` (
  `user rfid` varchar(30) NOT NULL,
  `permission id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user permissions`
--

INSERT INTO `user permissions` (`user rfid`, `permission id`) VALUES
('040a5192495a80', 4),
('c30a740b', 5);

-- --------------------------------------------------------

--
-- Structure de la table `users`
--

CREATE TABLE `users` (
  `rfid` varchar(30) NOT NULL,
  `first name` varchar(255) NOT NULL,
  `last name` varchar(255) NOT NULL,
  `picture` blob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `users`
--

INSERT INTO `users` (`rfid`, `first name`, `last name`, `picture`) VALUES
('040a5192495a80', 'Quentin', 'Beauchet', 0x000000a0ba4fbebf0000002079cfb43f00000020c199c13f000000e0d2b3ba3f00000040bdcdbfbf000000003be5a03f000000c070db9fbf00000080a285a2bf000000e0ddcebb3f00000040f958b0bf000000a04cc1cc3f00000080712a743f000000e0a056d1bf000000a05d45a73f00000080c7e7b9bf000000e0e3a2b63f000000a049d9bfbf00000000db43afbf00000060a4a4c0bf00000080c18e7abf00000080e08db63f000000205067b03f00000060c5f3693f0000000031dca03f00000020aa2bafbf000000403ea7d5bf000000c0875aa1bf000000c0f5bab2bf00000000ba7eb73f00000020cb93b9bf000000808c60913f000000203f2075bf00000000a6afbbbf00000000e94fa83f00000060302ca5bf000000205bf5b33f000000405398a9bf000000c09698b1bf000000408ca6c83f00000040042e9bbf000000002b96cdbf0000006097879c3f000000a0d12f94bf00000020ee0cd23f000000801b99c13f00000060dec5b23f000000200a524dbf00000020db8bb8bf00000080c143bc3f000000203c21d3bf000000400e4fae3f000000407b8dc73f000000e037c0bd3f000000e00d01b23f00000080c094ab3f000000805fe0cbbf000000609423b03f00000020c9e2b73f00000040369ac8bf00000080a1d1bc3f000000c04fb4af3f00000040e1b0c1bf000000e00263953f000000c02824a7bf00000040cea4c43f000000204016bc3f000000603407bcbf000000205055c0bf000000a02c39b73f0000008054fccdbf0000006048eb86bf0000002063e0c13f0000002060d4b0bf00000080f068c6bf000000c0da30d1bf000000c0f14b83bf000000c062bcdd3f0000000050b3c23f000000e0ed2cc7bf00000000ae5698bf000000402a5fb3bf00000040902b403f00000080b892b83f000000402d56be3f000000800babbbbf0000008083bdabbf00000040f834c9bf000000809108903f000000e0799cc43f0000004064b686bf000000205bf94d3f000000a0beaed03f000000409a3db03f000000a026f084bf000000200856933f00000000e457b03f0000006080ddbebf000000c028118bbf00000060ef4293bf00000080bb5884bf000000607130ac3f000000e0df7fbbbf00000020e8cd9b3f00000020f8657a3f00000060d7f4c7bf000000a0c7b7c83f00000000793da4bf00000060b4afaf3f000000c09948be3f0000004038f7acbf000000608301babf0000004092a7a03f000000c0587dcd3f000000a0dc89d1bf000000c0a4dfc93f000000c0d7dfc03f000000a0361aa73f00000000f991c33f000000e00d8bb23f000000607321c03f000000204a92b5bf00000040dee3aebf00000040c0c3c8bf0000002016aba9bf00000020b68594bf000000c00e66bbbf0000008055b79c3f00000020cd729d3f),
('c30a740b', 'ADMIN', 'ADMIN', NULL);

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `door permissions`
--
ALTER TABLE `door permissions`
  ADD KEY `permission id` (`permission id`),
  ADD KEY `door id` (`door id`);

--
-- Index pour la table `doors`
--
ALTER TABLE `doors`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`);

--
-- Index pour la table `user permissions`
--
ALTER TABLE `user permissions`
  ADD KEY `permission id` (`permission id`),
  ADD KEY `user rfid` (`user rfid`);

--
-- Index pour la table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`rfid`);

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `door permissions`
--
ALTER TABLE `door permissions`
  ADD CONSTRAINT `door permissions_ibfk_1` FOREIGN KEY (`permission id`) REFERENCES `permissions` (`id`),
  ADD CONSTRAINT `door permissions_ibfk_2` FOREIGN KEY (`door id`) REFERENCES `doors` (`id`);

--
-- Contraintes pour la table `user permissions`
--
ALTER TABLE `user permissions`
  ADD CONSTRAINT `user permissions_ibfk_1` FOREIGN KEY (`permission id`) REFERENCES `permissions` (`id`),
  ADD CONSTRAINT `user permissions_ibfk_2` FOREIGN KEY (`user rfid`) REFERENCES `users` (`rfid`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;