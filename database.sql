/* creation de la base de donneés */

DROP DATABASE IF EXISTS projet;
CREATE DATABASE projet;



/* creation des relations  */

CREATE TABLE projet.`admins` ( `id` INT NOT NULL , `username` VARCHAR(255) NOT NULL , `firstname` VARCHAR(255) NOT NULL , `lastname` VARCHAR(255) NOT NULL , `email` VARCHAR(255) NOT NULL , `password` VARCHAR(255) NOT NULL , PRIMARY KEY (`id`), UNIQUE (`username`));

CREATE TABLE projet.`types_vehicules` ( `idtype` INT NOT NULL , `marque` VARCHAR(255) NOT NULL , `modele` VARCHAR(255) NOT NULL , `carburant` VARCHAR(255) NOT NULL , `couleur` VARCHAR(255) NOT NULL , `climatisation` BOOLEAN NOT NULL, `prix` INT NOT NULL , PRIMARY KEY (`idtype`));

CREATE TABLE projet.`vehicules` ( `matricule` VARCHAR(255) NOT NULL , `idtype` INT NOT NULL , `disponible` BOOLEAN NOT NULL , PRIMARY KEY (`matricule`));

CREATE TABLE projet.`clients` ( `cin` VARCHAR(255) NOT NULL , `motdepasse` VARCHAR(255) NOT NULL , `permis` VARCHAR(255) NOT NULL , `prenom` VARCHAR(255) NOT NULL , `nom` VARCHAR(255) NOT NULL , `datenaissance` DATE NOT NULL , `telephone` VARCHAR(255) NOT NULL , `adresse` VARCHAR(255) NOT NULL , PRIMARY KEY (`cin`), UNIQUE (`permis`));

CREATE TABLE projet.`reservations` ( `idreservation` INT NOT NULL , `cin` VARCHAR(255) NOT NULL , `idtype` INT NOT NULL , `datedepart` DATETIME NOT NULL , `dateretour` DATETIME NOT NULL , `duree` INT NOT NULL, `total` INT NOT NULL , `acceptee` BOOLEAN NOT NULL , `vue` BOOLEAN NOT NULL , PRIMARY KEY (`idreservation`));

CREATE TABLE projet.`locations_courantes` ( `idreservation` INT NOT NULL , `matricule` VARCHAR(255) NOT NULL , `payee` BOOLEAN NOT NULL , PRIMARY KEY (`idreservation`));

/* remplissage de la base de données */

INSERT INTO `admins` (`id`, `username`, `firstname`, `lastname`, `email`, `password`) VALUES ('0', 'test', 'test', 'test', 'test@test.com', 'test12'), ('1', 'admin', 'Hamza', 'Ait Bourhim', 'hmzabourhim@gmail.com', 'hamza12'), ('2', 'admin2', 'Taha', 'Lechgar', 'tahamr08@gmail.com', 'taha12'), ('3', 'admin3', 'Hayat', 'Gouhi', 'gouhihayat4@gmail.com', 'hayat12'), ('4', 'admin4', 'Abdellah', 'Hallou', 'abdeallahhallou33@gmail.com', 'abdellah12');

INSERT INTO `types_vehicules` (`idtype`, `marque`, `modele`, `carburant`, `couleur`, `climatisation`, `prix`) VALUES ('0', 'AUDI', 'A1', 'diesel', 'gris', TRUE, '600'), ('1', 'CITROEN', 'C3', 'diesel', 'blanc', TRUE, '300'), ('2', 'FIAT', '500', 'diesel', 'rose', TRUE, '300'), ('3', 'FIAT', 'Punto', 'diesel', 'noir', TRUE, '300'), ('4', 'FORD', 'Fiesta', 'essence', 'bleu', TRUE, '300'), ('5', 'PEUGEOT', '208', 'diesel', 'gris', FALSE, '350'), ('6', 'RENAULT', 'Clio', 'diesel', 'blanc', TRUE, '300'), ('7', 'FIAT', '500 automatique', 'essence', 'blanc', TRUE, '350');

INSERT INTO `vehicules` (`matricule`, `idtype`, `disponible`) VALUES ('A1234', '0', FALSE), ('A555', '0', FALSE), ('A0013', '0', TRUE), ('A300', '1', TRUE), ('B1234', '1', TRUE), ('B1503', '1', TRUE), ('B666', '1', TRUE), ('B144', '2', TRUE), ('F4565', '2', TRUE), ('X123M', '3', TRUE), ('D123M', '4', TRUE), ('D1234', '4', TRUE), ('SSS12', '6', TRUE), ('CC56', '7', TRUE), ('CC45', '7', TRUE), ('K4520', '7', TRUE);

INSERT INTO `clients` (`cin`, `motdepasse`, `permis`, `prenom`, `nom`, `datenaissance`, `telephone`, `adresse`) VALUES ('ABCD1234', 'ABCD1234', 'ABCD1111', 'Ali', 'Kouakbi', '1985-03-27', '0522460560', 'bd Emile Zola ang. rue de Province 20310 Quartier: Belvédère Casablanca.'), ('EFGH5678', 'EFGH5678', 'EFGH2222', 'Ahmed', 'Khalid Taoufik', '1999-09-18', '0628537560', 'derb Sidi Maarouf IV (El Fida) rue 50 n°28 Grand Casablanca.'), ('IJKL9101112', 'IJKL9101112', 'IJKL3333', 'Sara', 'Fatihi', '2000-01-27', '0640193760', 'avenue Alger ang. rue Kairaouan 10020 Rabat.'), ('MNOP13141516', 'MNOP13141516', 'MNOP4444', 'Kamal', 'Hamoun', '1970-02-02', '0666401866', '639 bd. Abdelkrim ElKhattabi derb Chabab Mohammédia.');

INSERT INTO `reservations` (`idreservation`, `cin`, `idtype`, `datedepart`, `dateretour`, `duree`, `total`, `acceptee`, `vue`) VALUES ('0', 'ABCD1234', '0', '2020-09-01 21:14:08', '2020-09-03 21:14:08', '2', '1200', '1', '1'), ('1', 'ABCD1234', '7', '2020-09-01 21:14:08', '2020-09-03 21:14:08', '2', '700', '0', '1'), ('2', 'EFGH5678', '0', '2020-09-01 21:14:08', '2020-09-03 21:14:08', '2', '1200', '1', '1'), ('3', 'MNOP13141516', '3', '2020-09-01 21:14:08', '2020-09-03 21:14:08', '2', '600', '0', '0');

INSERT INTO `locations_courantes` (`idreservation`, `matricule`, `payee`) VALUES ('2', 'A1234', FALSE), ('0', 'A555', TRUE);
