alter table answer
    alter column submission_time set default current_timestamp;
alter table question
    alter column submission_time set default current_timestamp;
alter table comment
    alter column submission_time set default current_timestamp;
alter table users
    alter column registration_time set default current_timestamp;