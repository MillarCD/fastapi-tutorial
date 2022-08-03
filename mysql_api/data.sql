USE gestor_asignaturas;

INSERT INTO Tipos_evaluaciones VALUES('trabajo');
INSERT INTO Tipos_evaluaciones VALUES('prueba');

INSERT INTO Asignaturas VALUES(
  'info241',
  'bioinformatica'
);
INSERT INTO Asignaturas VALUES(
  'info248',
  'ingenieria de software'
);
INSERT INTO Asignaturas VALUES(
  'info257',
  'inteligencia artificial'
);

INSERT INTO Evaluaciones VALUES(
  'E1',
  'pp1',
  NULL,
  '2000-05-20',
  NULL,
  'info257',
  'prueba'
);
INSERT INTO Evaluaciones VALUES(
  'E2',
  'pp2',
  0.3,
  '2022-04-13',
  7,
  'info257',
  'trabajo'
);
INSERT INTO Evaluaciones VALUES(
  'E3',
  'pp3',
  0.4,
  '2000-03-12',
  NULL,
  'info248',
  'prueba'
);
INSERT INTO Evaluaciones VALUES(
  'E4',
  'pp5',
  0.2,
  '2000-04-12',
  NULL,
  'info241',
  'prueba'
);
