DELETE FROM question;
DELETE FROM answer;
DELETE FROM comment;
DELETE FROM users;

INSERT INTO question VALUES (1, '2020-05-01 10:41:00', 0, 4, 'Adoptation dilemma', 'Should I tell my parents I’m adopted?', NULL, 1);
INSERT INTO question VALUES (2, '2020-05-03 09:20:00', 0, -3, 'Cannibalism', 'If I eat myself, will I get twice as big or disappear completely?', NULL, 1);
INSERT INTO question VALUES (3, '2020-05-08 10:48:00', 0, 2, 'Space Battles', 'Do you think NASA invented thunderstorms to cover up the sound of space battles?', NULL, 1);
INSERT INTO question VALUES (4, '2020-05-11 15:41:00', 0, -1, 'Motherhood', 'How am I sure I’m the real mom of my kid?', NULL, 1);
INSERT INTO question VALUES (5, '2020-05-23 18:10:00', 0, 2, 'Travel', 'How far of a drive is it from Miami to Florida?', NULL, 1);
INSERT INTO question VALUES (6, '2020-06-03 22:09:00', 0, 0, 'Mathematics', 'What does a quarter until 4 mean? Like, why is it called that?! Because a quarter is worth 25 cents, so why is it 15 mins?!', NULL, 1);
INSERT INTO question VALUES (7, '2020-06-23 09:19:00', 0, -1, 'Biology Dilemma', 'Are chickens considered animals or birds?', NULL, 1);
INSERT INTO question VALUES (8, '2020-07-10 12:09:00', 0, 1, 'Genetics', 'Is it possible fro tattoos to get passed on genetically from paretnt to child?', NULL, 1);
INSERT INTO question VALUES (9, '2020-07-15 18:10:00', 0, 4, 'Shy dog', 'If I shave my golden retriever like a lion, will the other dogs respect him more?', NULL, 1);
INSERT INTO question VALUES (10, '2020-07-23 19:09:00', 0, 0, 'It’s sucks to lose a sock', 'Where do lost socks go when they go missing?', NULL, 1);
INSERT INTO question VALUES (11, '2020-08-06 11:19:00', 0, 1, 'Leap Year Problem', 'What happens to the people born on February 29????? Do the stay one until 4 years pass??', NULL, 1);
INSERT INTO question VALUES (12, '2020-08-23 18:10:00', 0, -1, 'Virtual Sunshine', 'Does looking at a picture of the sun hurt your eyes?', NULL, 1);
INSERT INTO question VALUES (13, '2020-09-03 11:19:00', 0, 0, 'How is it possible?', 'If Batman’s parents are dead, then how was he born?', NULL, 1);
INSERT INTO question VALUES (14, '2020-09-23 18:10:00', 0, 4, 'Ingredients', 'If corn oil is made from corn and vegetable oil is made from vegetables. What is baby oil made from?', NULL, 1);
INSERT INTO question VALUES (15, '2020-10-10 14:03:00', 0, 3, 'Let in or Outlet?', 'Why is an electrical socket called an outlet when you plug things into it?', NULL, 1);
SELECT pg_catalog.setval('question_id_seq', 15, true);

INSERT INTO answer VALUES (1, '2020-05-01 10:55:00', 3, 1, 'Idiot...', NULL, 2);
INSERT INTO answer VALUES (2, '2020-05-01 10:59:00', 0, 1, 'How old are you?', NULL, 2);
INSERT INTO answer VALUES (3, '2020-05-01 11:03:00', 0, 1, 'You should find the rigth moment to do so', 'Pngtreeexpression_emoticon_package_wink_cartoon_3803203.png', 2);
INSERT INTO answer VALUES (4, '2020-05-08 10:50:00', 2, 3, 'I do', NULL, 2);
INSERT INTO answer VALUES (5, '2020-05-08 10:55:00', 0, 3, 'The battle is real', 'b3155b97e9fbac5981919194a7d224be.jpg', 2);
INSERT INTO answer VALUES (6, '2020-05-23 18:20:00', 0, 5, 'You will get there in a few hours', NULL, 2);
INSERT INTO answer VALUES (7, '2020-05-23 18:42:00', 0, 5, 'It is too far, i would not go there', NULL, 2);
INSERT INTO answer VALUES (8, '2020-05-24 09:10:00', 1, 5, 'Bruh, Miami is in Florida', NULL, 2);
INSERT INTO answer VALUES (9, '2020-06-04 16:09:00', 0, 6, 'Fuck maths', NULL, 2);
INSERT INTO answer VALUES (10, '2020-07-10 15:19:00', 0, 8, 'There is typo dude', NULL, 2);
INSERT INTO answer VALUES (11, '2020-07-17 11:16:00', 3, 9, 'Mine already looks like one', 'maxresdefault.jpg', 2);
INSERT INTO answer VALUES (12, '2020-07-18 18:10:00', 0, 9, 'cuuuuuuuuute <3', NULL, 2);
INSERT INTO answer VALUES (13, '2020-08-09 01:14:00', 0, 11, 'Well, technically yes, but actually no', NULL, 2);
INSERT INTO answer VALUES (14, '2020-09-07 21:09:00', 0, 13, 'magic', NULL, 2);
INSERT INTO answer VALUES (15, '2020-09-24 08:16:00', 0, 14, 'you do not want to know', NULL, 2);
INSERT INTO answer VALUES (16, '2020-09-25 17:45:00', 0, 14, 'from babies, obviously', NULL, 2);
INSERT INTO answer VALUES (17, '2020-10-10 16:33:00', 4, 15, 'Let in sounds better', NULL, 2);
SELECT pg_catalog.setval('answer_id_seq', 17, true);

INSERT INTO comment VALUES(1, 1, NULL, 'Absolutely', '2020-08-09 01:14:00', 0, 3);
INSERT INTO comment VALUES(2, NULL , 1, 'You are the idiot', '2020-08-19 01:14:00', 2, 3);
INSERT INTO comment VALUES(3, 2, NULL, 'I hope you will disappear', '2021-06-09 01:14:00', 0, 3);
INSERT INTO comment VALUES(4, NULL , 3, 'Exactly', '2021-01-09 01:14:00', 0, 3);
INSERT INTO comment VALUES(5, 5, NULL, '2 inches', '2020-08-09 01:14:00', 0, 3);
INSERT INTO comment VALUES(6, NULL , 2, 'Eight and a half', '2022-01-09 01:14:00', 0, 3);
INSERT INTO comment VALUES(7, 6, NULL, 'What', '2021-4-09 01:14:00', 0, 3);
INSERT INTO comment VALUES(8, NULL , 8, 'Really?', '2021-10-09 01:14:00', 0, 3);
INSERT INTO comment VALUES(9, 9, NULL, 'No', '2021-08-11 01:14:00', 1, 3);
INSERT INTO comment VALUES(10, NULL , 4, 'Why', '2022-01-02 01:14:00', 0, 3);
INSERT INTO comment VALUES(11, 11, NULL, 'Yes', '2022-02-09 01:14:00', 0, 3);
INSERT INTO comment VALUES(12, NULL , 12, 'Noooo, you are cute', '2022-3-24 01:14:00', 1, 3);
SELECT pg_catalog.setval('comment_id_seq', 12, true);

INSERT INTO users (username, first_name, last_name, password, registration_time)
VALUES ('nyal_tamás@gmail.com', 'Nyal', 'Tamás', 'nyaltamas', '2018-04-20 09:44:40.154868');

INSERT INTO users (username, first_name, last_name, password, registration_time)
VALUES ('para_zita@gmail.com', 'Para', 'Zita', 'parazita', '2018-05-12 09:44:40.154868')

INSERT INTO users (username, first_name, last_name, password, registration_time)
VALUES ('nyomo_reka@gmail.com', 'Nyomo', 'Réka', 'nyomoreka', '2018-08-02 09:44:40.154868')

INSERT INTO users (username, first_name, last_name, password, registration_time)
VALUES ('remek_elek@gmail.com', 'Remek', 'Elek', 'remekelek', '2018-11-07 09:44:40.154868')

INSERT INTO users (username, first_name, last_name, password, registration_time)
VALUES ('paradi_csoma@gmail.com', 'Paradi', 'Csoma', 'paradicsoma', '2019-01-20 09:44:40.154868')

INSERT INTO users (username, first_name, last_name, password, registration_time)
VALUES ('fasomer_mitfizetskiy@gmail.com', 'Fasomer', 'Mitfizetskiy', 'fasomermitfizetskiy', '2019-03-11 09:44:40.154868')

INSERT INTO users (username, first_name, last_name, password, registration_time)
VALUES ('vak_cina@gmail.com', 'Vak', 'Cina', 'vakcina', '2020-04-20 09:44:40.154868')

INSERT INTO users (username, first_name, last_name, password, registration_time)
VALUES ('hu_jeno@gmail.com', 'Hü', 'Jenő', 'hujeno', '2022-02-17 09:44:40.154868')
