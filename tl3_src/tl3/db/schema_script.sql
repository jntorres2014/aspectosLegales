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
  CONSTRAINT FK_id FOREIGN KEY (id_user) REFERENCES users (id)
);

CREATE TABLE cookies(
  key character (20)PRIMARY KEY,
  value character(20) NOT NULL,
  ); 


insert into cookies (key,value)
values ('key','value');

INSERT INTO users (name, age, username, password) 
  VALUES ('Pedro Konstantinoff',36,'pedro','un_password'); 


SELECT * FROM users;
