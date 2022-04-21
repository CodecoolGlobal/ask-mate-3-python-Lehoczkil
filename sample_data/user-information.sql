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

INSERT INTO users (username, first_name, last_name, password, registration_time)
VALUES ('test.user@test.com', 'Test', 'User', '1234', '2022-04-20 09:44:40.154868')