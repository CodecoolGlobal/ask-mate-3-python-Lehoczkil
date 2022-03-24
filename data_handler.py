import csv
import calendar
import time
from datetime import datetime

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def read_questions(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows[::-1]


def write_questions(filename, line):
    last_id = len(read_questions(filename))
    timestamp = calendar.timegm(time.gmtime())
    line.insert(0, last_id + 1)
    line.insert(1, timestamp)
    with open(filename, 'a', newline='') as f:
        fieldnames = QUESTION_HEADER
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        new_row = dict(zip(QUESTION_HEADER, line))
        writer.writerow(new_row)


def write_answer(filename, line):
    last_id = len(read_questions(filename))
    timestamp = calendar.timegm(time.gmtime())
    line.insert(0, last_id + 1)
    line.insert(1, timestamp)
    with open(filename, 'a', newline='') as f:
        fieldnames = ANSWER_HEADER
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        new_row = dict(zip(ANSWER_HEADER, line))
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
    all_questions = read_questions('sample_data/question.csv')
    converted_dates = []
    for question in all_questions:
        question_date = int(question[QUESTION_HEADER[1]])
        converted_dates.append(datetime.fromtimestamp(question_date))
    return converted_dates
