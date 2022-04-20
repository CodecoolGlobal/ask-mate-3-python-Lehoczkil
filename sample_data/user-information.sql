--------------------------------------- Store data for user-information ------------------------------------------------
DROP TABLE IF EXISTS public.users;
CREATE TABLE users (
    id serial NOT NULL,
    username text,
    first_name text,
    last_name text,
    password text,
    registration_time timestamp without time zone
);

INSERT INTO users (username, first_name, last_name, password)
VALUES ('TestUser', 'Test', 'User', '1234')