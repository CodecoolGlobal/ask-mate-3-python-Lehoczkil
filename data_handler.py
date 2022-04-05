import csv
import calendar
import time
from datetime import datetime
import database_common
from psycopg2 import sql


QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def read_file(filename):
    with open(filename, 'r') as f:
        return [row for row in csv.DictReader(f)]


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


def write_to_file(filename, line, headers):
    id_s = [int(question[headers[0]]) for question in read_file(filename)]
    try:
        last_id = max(id_s)
    except ValueError:
        last_id = 0
    timestamp = calendar.timegm(time.gmtime())
    line.insert(0, last_id + 1)
    line.insert(1, timestamp)
    with open(filename, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        new_row = dict(zip(headers, line))
        writer.writerow(new_row)


@database_common.connection_handler
def add_answer(cursor, submission_time, question_id, message, image):
    cursor.execute(f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES ('{submission_time}', 0, {question_id}, '{message}', '{image}');""")


@database_common.connection_handler
def add_question(cursor, submission_time, title, message, image):
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


def convert_date():
    questions = read_file('sample_data/question.csv')
    converted_dates = []
    for question in questions:
        question_date = int(question[QUESTION_HEADER[1]])
        converted_dates.append(datetime.fromtimestamp(question_date))
    return converted_dates
