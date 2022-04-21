--------------------------------------- Store data for user-reputation ------------------------------------------------
DROP TABLE IF EXISTS public.reputation;
CREATE TABLE reputation (
    user_id integer NOT NULL,
    reputation_points integer NOT NULL);