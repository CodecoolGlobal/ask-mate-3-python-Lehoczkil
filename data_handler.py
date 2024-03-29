import database_common
import bcrypt
from psycopg2 import sql


@database_common.connection_handler
def read_table(cursor, table_name, order_method='submission_time', order_type='DESC'):
    cursor.execute(sql.SQL("""
    SELECT * 
    FROM {table_name}
    ORDER BY {order_method} {order_type}
    """).format(table_name=sql.Identifier(table_name),
                order_method=sql.Identifier(order_method), order_type=sql.SQL(order_type)))
    return cursor.fetchall()


@database_common.connection_handler
def search_by_id(cursor, table_name, column, question_id, order='id'):
    cursor.execute(sql.SQL("""
    SELECT *
    FROM {table_name}
    WHERE {column} = {question_id}
    ORDER BY {order}
    """).format(table_name=sql.Identifier(table_name), column=sql.Identifier(column),
                question_id=sql.Literal(question_id), order=sql.Identifier(order)))
    data_by_id = cursor.fetchall()
    return [dict(detail) for detail in data_by_id]


@database_common.connection_handler
def delete_record(cursor, table_name, record_id):
    cursor.execute(sql.SQL("""
    DELETE FROM {table_name}
    WHERE id = {record_id}
    """).format(table_name=sql.Identifier(table_name), record_id=sql.Literal(record_id)))


@database_common.connection_handler
def add_question(cursor, question_fields):
    title, message, user_id, image = question_fields
    cursor.execute(sql.SQL("""
        INSERT INTO question (view_number, vote_number, title, message, image, user_id)
        VALUES ({view_number}, {vote_number}, {title}, {message}, {image}, {user_id})
        """).format(view_number=sql.Literal(0),
                    vote_number=sql.Literal(0),
                    title=sql.Literal(title),
                    message=sql.Literal(message),
                    image=sql.Literal(image),
                    user_id=sql.Literal(user_id)))


@database_common.connection_handler
def add_answer(cursor, new_answer_data_items):
    question_id, message, user_id, image = new_answer_data_items
    cursor.execute(sql.SQL("""
        INSERT INTO "answer" (vote_number, question_id, message, image, user_id)
        VALUES ({vote_number}, {question_id}, {message}, {image}, {user_id})
        """).format(vote_number=sql.Literal(0),
                    question_id=sql.Literal(question_id),
                    message=sql.Literal(message),
                    image=sql.Literal(image),
                    user_id=sql.Literal(user_id)))


@database_common.connection_handler
def update_answer(cursor, answer_id, message):
    cursor.execute(sql.SQL("""
        UPDATE answer
        SET "message"={message}
        WHERE id = {answer_id}
        """).format(answer_id=sql.Literal(answer_id), message=sql.Literal(message)))


@database_common.connection_handler
def update_question(cursor, question_id, updated_title, updated_message):
    cursor.execute(sql.SQL("""
    UPDATE question
    SET "title"={title}, "message"={message}
    WHERE id = {question_id}
    """).format(title=sql.Literal(updated_title), message=sql.Literal(updated_message), question_id=sql.Literal(question_id)))


@database_common.connection_handler
def add_comment_to_question(cursor, question_id, message, user_id):
    cursor.execute(sql.SQL("""
    INSERT INTO comment (question_id, message, edited_count, user_id)
    VALUES ({question_id}, {message}, {edited_count}, {user_id})
    """).format(question_id=sql.Literal(question_id),
                message=sql.Literal(message),
                edited_count=sql.Literal(0),
                user_id=sql.Literal(user_id)))


@database_common.connection_handler
def add_comment_to_answer(cursor, answer_id, message, user_id):
    cursor.execute(sql.SQL("""
    INSERT INTO comment (answer_id, message, edited_count, user_id)
    VALUES ({answer_id}, {message}, {edited_count}, {user_id})
    """).format(answer_id=sql.Literal(answer_id),
                message=sql.Literal(message),
                edited_count=sql.Literal(0),
                user_id=sql.Literal(user_id)))


@database_common.connection_handler
def edit_comment(cursor, comment_id, message,):
    cursor.execute(sql.SQL("""
    UPDATE comment
    SET "message" = {message}, edited_count = edited_count + 1
    WHERE id = {comment_id}""").format(comment_id=sql.Literal(comment_id), message=sql.Literal(message)))


@database_common.connection_handler
def delete_comment(cursor, comment_id):
    cursor.execute(sql.SQL("""
    DELETE FROM comment
    WHERE id={comment_id}""").format(comment_id=sql.Literal(comment_id)))


@database_common.connection_handler
def vote_up(cursor, table_name, selected_id):
    cursor.execute(sql.SQL("""
    UPDATE {column_name}
    SET vote_number = vote_number + 1
    WHERE id={selected_id}""").format(selected_id=sql.Literal(selected_id), column_name=sql.Identifier(table_name)))


@database_common.connection_handler
def vote_down(cursor, table_name, selected_id):
    cursor.execute(sql.SQL("""
    UPDATE {column_name}
    SET vote_number = vote_number - 1
    WHERE id={selected_id}""").format(selected_id=sql.Literal(selected_id), column_name=sql.Identifier(table_name)))


@database_common.connection_handler
def get_question_by_answer_id(cursor, answer_id):
    cursor.execute(sql.SQL("""
    SELECT question_id
    FROM answer
    WHERE id={answer_id}""").format(answer_id=sql.Literal(answer_id)))
    data = cursor.fetchall()
    return [dict(detail) for detail in data]


@database_common.connection_handler
def add_tag_to_table(cursor, new_tag):
    cursor.execute(sql.SQL("""
    INSERT INTO tag (name) 
    VALUES ({new_tag}) RETURNING id""").format(new_tag=sql.Literal(new_tag)))
    return cursor.fetchone()['id']


@database_common.connection_handler
def add_tag_to_question(cursor, question_id, tag_id):
    cursor.execute(sql.SQL("""
        INSERT INTO question_tag (question_id, tag_id)
        VALUES ({question_id}, {tag_id})""").format(question_id=sql.Literal(question_id), tag_id=sql.Literal(tag_id)))


@database_common.connection_handler
def get_tag(cursor):
    cursor.execute("""
        SELECT name
        FROM tag""")
    return cursor.fetchall()


@database_common.connection_handler
def find_search_results(cursor, expression):
    cursor.execute(sql.SQL("""
        SELECT DISTINCT question.*
        FROM question
        LEFT JOIN answer ON question.id = answer.question_id
        WHERE question.title ILIKE {expression} OR question.message ILIKE {expression} OR answer.message ILIKE {expression}""").format(expression=sql.Literal('%' + expression + '%')))
    return cursor.fetchall()


@database_common.connection_handler
def delete_tag(cursor, tag_id):
    cursor.execute(sql.SQL("""
        DELETE FROM tag
        WHERE id = {tag_id}
        """).format(tag_id=sql.Literal(tag_id)))


@database_common.connection_handler
def display_latest_question(cursor):
    cursor.execute(sql.SQL("""
        SELECT * 
        FROM question
        ORDER BY submission_time DESC
        LIMIT 5
        """))
    return cursor.fetchall()


@database_common.connection_handler
def get_question_tags(cursor, question_id):
    cursor.execute(sql.SQL("""
        SELECT *
        FROM tag
        INNER JOIN question_tag ON tag.id = question_tag.tag_id
        WHERE question_tag.question_id = {question_id}
        """).format(question_id=sql.Literal(question_id)))
    return cursor.fetchall()


def hash_password(plain_text_password):
    # By using bcrypt, the salt is saved into the hash itself
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def add_user(cursor, username, first_name, last_name, password):
    cursor.execute(sql.SQL("""
        INSERT INTO users (username, first_name, last_name, password)
        VALUES({username}, {first_name}, {last_name}, {password})
        """).format(username=sql.Literal(username),
                    first_name=sql.Literal(first_name),
                    last_name=sql.Literal(last_name),
                    password=sql.Literal(password)))

    cursor.execute(sql.SQL("""
        SELECT id FROM users
        WHERE username = {username}""").format(username=sql.Literal(username)))
    new_user_id = cursor.fetchone()['id']

    cursor.execute(sql.SQL("""
        INSERT INTO reputation (user_id, reputation_points) VALUES ({new_user_id}, 0)
    """).format(new_user_id=sql.Literal(new_user_id)))


@database_common.connection_handler
def get_users(cursor):
    cursor.execute(sql.SQL("""
    SELECT username
    FROM users
    ORDER BY id"""))
    return cursor.fetchall()


@database_common.connection_handler
def get_password_by_username(cursor, input_username):
    cursor.execute('''
    SELECT password
    FROM users
    WHERE username = %(username)s;''', {'username': input_username})
    return cursor.fetchone()


@database_common.connection_handler
def list_users(cursor):
    cursor.execute(sql.SQL("""
        SELECT users.username, TO_CHAR(users.registration_time :: DATE, 'yyyy.mm.dd') AS registration_time,
       COUNT(question.user_id) AS number_of_questions
        FROM users
        LEFT JOIN question ON users.id = question.user_id
        GROUP BY users.username, users.registration_time;"""))
    user_reg_num_of_questions = cursor.fetchall()
    user_attributes = [dict(detail) for detail in user_reg_num_of_questions]

    cursor.execute(sql.SQL("""
        SELECT users.username, COUNT(answer.user_id) AS number_of_answers
        FROM users
        LEFT JOIN answer on users.id = answer.user_id
        GROUP BY users.username;"""))
    num_of_answers = cursor.fetchall()

    cursor.execute(sql.SQL("""
        SELECT users.username, COUNT(comment.user_id) AS number_of_comments
        FROM users
        LEFT JOIN comment on users.id = comment.user_id
        GROUP BY users.username;"""))
    num_of_comments = cursor.fetchall()

    cursor.execute(sql.SQL("""
        SELECT users.username, reputation.reputation_points AS reputation_points
        FROM users
        LEFT JOIN reputation on users.id = reputation.user_id
        GROUP BY users.username, reputation.reputation_points;"""))
    reputation_points = cursor.fetchall()

    for attributes in user_attributes:
        for data in num_of_answers:
            if data['username'] == attributes['username']:
                attributes.update(data)
        for data in num_of_comments:
            if data['username'] == attributes['username']:
                attributes.update(data)
        for data in reputation_points:
            if data['username'] == attributes['username']:
                attributes.update(data)

    return user_attributes


@database_common.connection_handler
def get_user_data(cursor, user_id):

    cursor.execute(sql.SQL("""
            SELECT CONCAT(first_name,' ', last_name)
            FROM users
            WHERE id = {user_id}""").format(user_id=sql.Literal(user_id)))
    name = [dict(detail) for detail in cursor.fetchall()]

    cursor.execute(sql.SQL("""
                SELECT username
                FROM users
                WHERE id = {user_id}""").format(user_id=sql.Literal(user_id)))
    username = [dict(detail) for detail in cursor.fetchall()]

    cursor.execute(sql.SQL("""
            SELECT registration_time
            FROM users
            WHERE id = {user_id}""").format(user_id=sql.Literal(user_id)))
    registration_date = [dict(detail) for detail in cursor.fetchall()]

    cursor.execute(sql.SQL("""
           SELECT COUNT(answer.user_id) AS number_of_answers
            FROM answer
            WHERE answer.user_id = {user_id};""").format(user_id=sql.Literal(user_id)))
    num_of_answers = [dict(detail) for detail in cursor.fetchall()]

    cursor.execute(sql.SQL("""
               SELECT COUNT(question.user_id) AS number_of_questions
                FROM question
                WHERE question.user_id = {user_id};""").format(user_id=sql.Literal(user_id)))
    num_of_question = [dict(detail) for detail in cursor.fetchall()]

    cursor.execute(sql.SQL("""
               SELECT COUNT(comment.user_id) AS number_of_comments
                FROM comment
                WHERE comment.user_id = {user_id};""").format(user_id=sql.Literal(user_id)))
    num_of_comment = [dict(detail) for detail in cursor.fetchall()]

    cursor.execute(sql.SQL("""
                   SELECT reputation_points
                    FROM reputation
                    WHERE reputation.user_id = {user_id};""").format(user_id=sql.Literal(user_id)))
    reputation_points = [dict(detail) for detail in cursor.fetchall()]

    return [user_id,
            name[0]['concat'],
            username[0]['username'],
            registration_date[0]['registration_time'],
            num_of_question[0]['number_of_questions'],
            num_of_answers[0]['number_of_answers'],
            num_of_comment[0]['number_of_comments'],
            reputation_points]


@database_common.connection_handler
def calculate_reputation_points_of_user(cursor, user_id):
    cursor.execute(sql.SQL("""
        SELECT SUM(question.vote_number) * 5 AS question
        FROM users
        LEFT JOIN question ON users.id = question.user_id
        WHERE users.id = {user_id}""").format(user_id=sql.Literal(user_id)))
    reputation_points_on_questions = cursor.fetchone()['question'] or 0

    cursor.execute(sql.SQL("""
        SELECT SUM(answer.vote_number) * 10 as answer
        FROM users
        LEFT JOIN answer ON users.id = answer.user_id
        WHERE users.id = {user_id}""").format(user_id=sql.Literal(user_id)))
    reputation_points_on_answers = cursor.fetchone()['answer'] or 0

    sum_of_reputation_points = reputation_points_on_questions + reputation_points_on_answers
    set_reputation_points_of_user(user_id, sum_of_reputation_points)


@database_common.connection_handler
def set_reputation_points_of_user(cursor, user_id, sum_of_reputation_points):
    cursor.execute(sql.SQL("""
        UPDATE reputation
        SET reputation_points = {sum_of_reputation_points}
        WHERE reputation.user_id = {user_id}
        """).format(sum_of_reputation_points=sql.Literal(sum_of_reputation_points), user_id=sql.Literal(user_id)))


@database_common.connection_handler
def get_actual_reputation_points_of_user(cursor, user_id):
    cursor.execute(sql.SQL("""
        SELECT reputation_points FROM reputation
        WHERE reputation.user_id = {user_id}
        """).format(user_id=sql.Literal(user_id)))
    return cursor.fetchone()['reputation_points']


@database_common.connection_handler
def lose_reputation_points(cursor, user_id, reputation_points):
    cursor.execute(sql.SQL("""
        UPDATE reputation
        SET reputation_points = {reputation_points} - 2
        WHERE user_id = {user_id}""").format(reputation_points=sql.Literal(reputation_points), user_id=sql.Literal(user_id)))


@database_common.connection_handler
def get_logged_in_user_id(cursor, username):
    cursor.execute(sql.SQL("""
        SELECT id FROM users
        WHERE username = {username}""").format(username=sql.Literal(username)))
    return cursor.fetchall()


@database_common.connection_handler
def get_question_id_by_tag_id(cursor, tag_id):
    cursor.execute(sql.SQL("""
    SELECT question_id
    FROM question_tag
    WHERE tag_id = {tag_id}
    """).format(tag_id=sql.Literal(tag_id)))
    return cursor.fetchall()


@database_common.connection_handler
def get_tag_id(cursor, tag_name):
    cursor.execute(sql.SQL("""
    SELECT id
    FROM tag
    WHERE name = {tag_name}
    """).format(tag_name=sql.Literal(tag_name)))
    return cursor.fetchall()


@database_common.connection_handler
def raise_view_count(cursor, question_id, view_number):
    cursor.execute(sql.SQL("""
    UPDATE question
    SET view_number = {view_number} + 1
    WHERE id = {question_id}
    """).format(question_id=sql.Literal(question_id), view_number=sql.Literal(view_number)))


@database_common.connection_handler
def get_user_id(cursor, username):
    cursor.execute(sql.SQL("""
        SELECT id
        FROM users
        WHERE username = {username}""").format(username=sql.Literal(username)))
    return cursor.fetchall()
