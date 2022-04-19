--------------------------------------- Store data for user-information ------------------------------------------------
DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    username text,
    first_name text,
    last_name text,
    password varchar(200) NOT NULL,
    registration_time timestamp without time zone
);

INSERT INTO users
VALUES (0, 'hello@world.com', 'Hello', 'World', 'b''$2b$12$4NSiuW6XzR35VfFxQE0RzOyU7NvTUkj3WKNZKWeeepZMg.ss01Rzq''')