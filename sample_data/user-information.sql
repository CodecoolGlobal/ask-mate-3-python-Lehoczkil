--------------------------------------- Store data for user-information ------------------------------------------------
DROP TABLE IF EXISTS ONLY public.users;
CREATE TABLE users (
    id serial NOT NULL,
    username text,
    first_name text,
    last_name text,
    password text,
    registration_time timestamp without time zone
);