CREATE TABLE users(
    id serial PRIMARY KEY, 
    name character(70) NOT NULL,
    username character(70) NOT NULL,
    age integer NOT NULL, 
    password character(20) NOT NULL
);

CREATE TABLE jobs(
  id serial PRIMARY KEY,
  id_user integer NOT NULL,
  lugar_trabajo character (70) NOT NULL,
  fecha_inicio Date NOT NULL,
  fecha_fin Date NOT NULL,
  cargo character (70) NOT NULL,
  observacion character (70),
  CONSTRAINT FK_id FOREIGN KEY id_users REFERENCES users (id),
  CONSTRAINT ch_fecha CHECK fecha_inicio < fecha_fin
);

CREATE TABLE cookies(
  key character (20)PRIMARY KEY,
  value character(20) NOT NULL,
); 


INSERT INTO users (name, age, username, password) 
  VALUES ('Pedro Konstantinoff',36,'pedro','un_password'); 

INSERT INTO jobs (lugar_trabajo, cargo, fecha_inicio, fecha_fin, observacion)
  VALUES (1,'La anonima','gerente', 2020-10-11,2021-10-11,"Trabaja bien");

SELECT * FROM users;

Select * FROM jobs;
