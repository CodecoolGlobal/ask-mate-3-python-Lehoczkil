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
