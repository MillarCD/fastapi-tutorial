DROP DATABASE IF EXISTS gestor_asignaturas;

CREATE DATABASE gestor_asignaturas;

USE gestor_asignaturas;

CREATE TABLE `Asignaturas` (
  `code` VARCHAR(20) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`code`)
);

CREATE TABLE `Tipos_evaluaciones` (
  `type_name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`type_name`)
);

CREATE TABLE `Evaluaciones` (
  `id` VARCHAR(5) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `value` FLOAT,
  `date` DATE,
  `note` FLOAT,
  `code` VARCHAR(20) NOT NULL,
  `type` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`code`) REFERENCES Asignaturas(`code`),
  FOREIGN KEY (`type`) REFERENCES Tipos_evaluaciones(`type_name`)
);
