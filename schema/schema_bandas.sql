-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema schema_banda
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `schema_banda` ;

-- -----------------------------------------------------
-- Schema schema_banda
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `schema_banda` DEFAULT CHARACTER SET utf8 ;
USE `schema_banda` ;

-- -----------------------------------------------------
-- Table `schema_banda`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `schema_banda`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NULL,
  `apellido` VARCHAR(255) NULL,
  `email` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `schema_banda`.`bandas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `schema_banda`.`bandas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_banda` VARCHAR(255) NULL,
  `genero_musical` VARCHAR(255) NULL,
  `ciudad_origen` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_bandas_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_bandas_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `schema_banda`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
