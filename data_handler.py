import csv
import calendar
import time

DATA_HEADER = ['id', 'submission time', 'view number', 'vote number', 'title', 'message', 'image']


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
        fieldnames = DATA_HEADER
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        new_row = dict(zip(DATA_HEADER, line))
        writer.writerow(new_row)
