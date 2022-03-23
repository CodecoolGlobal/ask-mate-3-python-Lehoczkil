import csv
import calendar
import time

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'title', 'message', 'image']


def read_questions(filename):
    rows = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows[::-1]


def write_questions(filename, line):
    last_id = len(read_questions(filename))-1
    timestamp = calendar.timegm(time.gmtime())
    line.insert(0, last_id + 1)
    line.insert(1, timestamp)
    with open(filename, 'a', newline='') as f:
        fieldnames = QUESTION_HEADER
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        new_row = dict(zip(QUESTION_HEADER, line))
        writer.writerow(new_row)


def delete_line(filename, line):
    with open(filename, 'w', newline='') as f:
        if filename == 'sample_data/answer.csv':
            fieldnames = ANSWER_HEADER
        elif filename == 'sample_data/question.csv':
            fieldnames = QUESTION_HEADER
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for data in line:
            writer.writerow(data)
