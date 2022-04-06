import database_common
from psycopg2 import sql


@database_common.connection_handler
def read_table(cursor, table_name, order_method='submission_time', order_type='DESC'):
    cursor.execute(sql.SQL("""
    SELECT * 
    FROM {table_name}
    ORDER BY {order_method} {order_type}
    """).format(table_name=sql.Identifier(table_name), order_method=sql.Identifier(order_method), order_type=sql.SQL(order_type)))
    return cursor.fetchall()


@database_common.connection_handler
def search_by_id(cursor, table_name, column, question_id):
    cursor.execute(sql.SQL("""
    SELECT *
    FROM {table_name}
    WHERE {column} = {question_id}
    """).format(table_name=sql.Identifier(table_name), column=sql.Identifier(column), question_id=sql.Literal(question_id)))
    data_by_id = cursor.fetchall()
    return [dict(detail) for detail in data_by_id]


@database_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute(sql.SQL("""
    DELETE FROM question
    WHERE id = {question_id}
    """).format(question_id=sql.Literal(question_id)))


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute(sql.SQL("""
    DELETE FROM answer
    WHERE id = {answer_id}
    """).format(answer_id=sql.Literal(answer_id)))


@database_common.connection_handler
def add_question(cursor, title, message, image):
    cursor.execute(sql.SQL("""
        INSERT INTO question (view_number, vote_number, title, message, image)
        VALUES ({view_number}, {vote_number}, {title}, {message}, {image})
        """).format(view_number=sql.Literal(0), vote_number=sql.Literal(0), title=sql.Literal(title), message=sql.Literal(message), image=sql.Literal(image)))


@database_common.connection_handler
def add_answer(cursor, question_id, message, image):
    cursor.execute(sql.SQL("""
        INSERT INTO "answer" (vote_number, question_id, message, image)
        VALUES ({vote_number}, {question_id}, {message}, {image})
        """).format(vote_number=sql.Literal(0), question_id=sql.Literal(question_id), message=sql.Literal(message), image=sql.Literal(image)))


@database_common.connection_handler
def update_question(cursor, question_id, updated_title, updated_message):
    cursor.execute(sql.SQL("""
    UPDATE question
    SET "title"={title}, "message"={message}
    WHERE id = {question_id}
    """).format(title=sql.Literal(updated_title), message=sql.Literal(updated_message), question_id=sql.Literal(question_id)))


@database_common.connection_handler
def get_comment_data(cursor, comment_id):
    cursor.execute(sql.SQL("""
    SELECT *
    FROM comment
    WHERE id = {comment_id}
    """).format(comment_id=sql.Literal(comment_id)))
    return cursor.fetchall()