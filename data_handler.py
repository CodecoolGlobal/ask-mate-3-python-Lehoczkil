import datetime
import database_common
from psycopg2 import sql


@database_common.connection_handler
def read_table(cursor, table_name, order_method='submission_time', order_type='DESC'):
    query = f"""
        SELECT * 
        FROM {table_name}
        ORDER BY {order_method} {order_type}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def search_by_id(cursor, table_name, column, question_id):
    query = f"""
        SELECT *
        FROM {table_name}
        WHERE {column} = {question_id}"""
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def delete_question(cursor, question_id):
    query = f"""
        DELETE 
        FROM question
        WHERE id ={question_id}
        """
    cursor.execute(query)


@database_common.connection_handler
def add_answer(cursor, question_id, message, image):
    submission_time = datetime.datetime.today()
    cursor.execute(f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES ('{submission_time}', 0, {question_id}, '{message}', '{image}');""")


@database_common.connection_handler
def add_question(cursor, title, message, image):
    submission_time = datetime.datetime.today()
    cursor.execute(f"""
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES ('{submission_time}', 0, 0, '{title}', '{message}', '{image}');""")


@database_common.connection_handler
def update_question(cursor, question_id, updated_title, updated_message):
    query = f"""
        UPDATE question 
        SET  title = '{updated_title}', message = '{updated_message}'
        WHERE id = '{question_id}'
        """
    cursor.execute(query)
