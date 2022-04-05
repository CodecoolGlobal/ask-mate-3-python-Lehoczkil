import datetime

from flask import Flask, render_template, redirect, url_for, request
import data_handler
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index_page():
    return render_template('index.html')


@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html')


@app.route('/about-us')
def about_us_page():
    return render_template('about-us.html')


@app.route('/list', methods=['GET', 'POST'])
def list_questions_page():
    questions = data_handler.read_table('question')
    headers = data_handler.QUESTION_HEADER

    if request.method == 'POST':
        select_id = request.form.get('select_sort')
        questions = data_handler.read_table('question', select_id)

        return redirect(url_for('list_questions_page', questions=questions, headers=headers))
    return render_template('list.html', questions=questions, headers=headers)


@app.route('/question/<question_id>')
def question_details_page(question_id=None):
    questions = data_handler.search_by_id('question', 'id', question_id)
    answers = data_handler.search_by_id('answer', 'question_id', question_id)
    return render_template('question_details.html', questions=questions, answers=answers)


@app.route('/question/<question_id>/delete')
def delete_question(question_id=None):
    data_handler.delete_question(question_id)
    return redirect(url_for('list_questions_page'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_image(fields, data):
    for field in fields:
        if field == 'image':
            image_file = request.files.get('image')
            if image_file and allowed_file(image_file.filename):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                data.append(filename)
        else:
            data.append(request.form.get(field))
    return data


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    submission_time = datetime.datetime.today()
    title = request.form.get('title')
    message = request.form.get('message')
    image = request.form.get('image')
    if request.method == 'POST':
        data_handler.add_question(submission_time, title, message, image)
        return redirect(url_for('list_questions_page'))
    return render_template('add_question.html')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id=None):
    questions = data_handler.read_file('sample_data/question.csv')
    edited_questions = []
    question_needed = {}
    if request.method == 'POST':
        for question in questions:
            if question['id'] == question_id:
                question['title'] = request.form.get('title')
                question['message'] = request.form.get('message')
            edited_questions.append(question)
        data_handler.update_line('sample_data/question.csv', edited_questions)
        return redirect(url_for('question_details_page', question_id=question_id))

    for question in questions:
        if question['id'] == question_id:
            question_needed = question
    return render_template('edit_question.html', question=question_needed)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    question = data_handler.search_by_id('question', 'id', question_id)
    submission_time = datetime.datetime.today()
    message = request.form.get('message')
    image = request.form.get('image')
    if request.method == 'POST':
        data_handler.add_answer(submission_time, question_id, message, image)
        return redirect(url_for('question_details_page', question_id=question_id))
    return render_template('post_answer.html', question=question)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id=None):
    answers = data_handler.read_file('sample_data/answer.csv')
    edited_answers = [answer for answer in answers if answer['id'] != answer_id]
    question_id = 0
    for answer in answers:
        if answer['id'] == answer_id:
            question_id = answer['question_id']
    data_handler.update_line('sample_data/answer.csv', edited_answers)
    return redirect(url_for('question_details_page', question_id=question_id))


def question_vote(direction, question_id):
    questions = data_handler.read_file('sample_data/question.csv')
    edited_questions = []
    for question in questions:
        if question['id'] == question_id:
            if direction == 'up':
                question['vote_number'] = int(question['vote_number']) + 1
            else:
                question['vote_number'] = int(question['vote_number']) - 1
            edited_questions.append(question)
        else:
            edited_questions.append(question)
    data_handler.update_line('sample_data/question.csv', edited_questions)


@app.route('/question/<question_id>/vote-down', methods=['GET', 'POST'])
def question_vote_down(question_id=None):
    question_vote('down', question_id)
    return redirect(url_for('list_questions_page'))


@app.route('/question/<question_id>/vote-up', methods=['GET', 'POST'])
def question_vote_up(question_id=None):
    question_vote('up', question_id)
    return redirect(url_for('list_questions_page'))


def answer_vote(direction, answer_id):
    answers = data_handler.read_file('sample_data/answer.csv')
    edited_answers = []
    question_id = 0
    for answer in answers:
        if answer['id'] == answer_id:
            question_id = answer['question_id']
            if direction == 'up':
                answer['vote_number'] = int(answer['vote_number']) + 1
            else:
                answer['vote_number'] = int(answer['vote_number']) - 1
            edited_answers.append(answer)
        else:
            edited_answers.append(answer)
    data_handler.update_line('sample_data/answer.csv', edited_answers)
    return question_id


@app.route('/answer/<answer_id>/vote-up', methods=['GET', 'POST'])
def answer_vote_up(answer_id=None):
    question_id = answer_vote('up', answer_id)
    return redirect(url_for('question_details_page', question_id=question_id))


@app.route('/answer/<answer_id>/vote-down', methods=['GET', 'POST'])
def answer_vote_down(answer_id=None):
    question_id = answer_vote('down', answer_id)
    return redirect(url_for('question_details_page', question_id=question_id))


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5200
    )
