import csv
import calendar
import time
from datetime import datetime
import database_common


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


def update_line(filename, line):
    with open(filename, 'w', newline='') as f:
        if filename == 'sample_data/answer.csv':
            fieldnames = ANSWER_HEADER
        elif filename == 'sample_data/question.csv':
            fieldnames = QUESTION_HEADER
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for data in line:
            writer.writerow(data)


def convert_date():
    questions = read_file('sample_data/question.csv')
    converted_dates = []
    for question in questions:
        question_date = int(question[QUESTION_HEADER[1]])
        converted_dates.append(datetime.fromtimestamp(question_date))
    return converted_dates
