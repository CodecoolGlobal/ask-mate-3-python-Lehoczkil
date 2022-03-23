from flask import Flask, render_template, redirect, url_for, request
import data_handler
import os
from werkzeug.utils import secure_filename
from datetime import date as dt

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list')
def list_page():
    questions = data_handler.read_questions('sample_data/question.csv')
    headers = data_handler.QUESTION_HEADER
    return render_template('list.html', questions=questions, headers=headers)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def questions_page(question_id=None):
    all_questions = data_handler.read_questions('sample_data/question.csv')
    question = {}
    for quest in all_questions:
        if quest['id'] == question_id:
            question = quest
    all_answers = data_handler.read_questions('sample_data/answer.csv')
    answers = []
    for ans in all_answers:
        if ans['question_id'] == question_id:
            answers.append(ans)
    return render_template('questions.html', question=question, answers=answers)


@app.route('/question/<question_id>/delete')
def delete_question(question_id=None):
    all_questions = data_handler.read_questions('sample_data/question.csv')
    new_all_questions = []
    for quest in all_questions:
        if quest['id'] == question_id:
            continue
        else:
            new_all_questions.append(quest)
    data_handler.delete_line('sample_data/question.csv', new_all_questions)
    return redirect('/list')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    question_fields = ['title', 'message', 'image']
    new_question_data_items = ['view', 'vote']
    if request.method == 'POST':
        for field in question_fields:
            if field == 'image':
                image_file = request.files['image']
                if image_file and allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    new_question_data_items.append(image_file.filename)
            else:
                new_question_data_items.append(request.form[field])
        data_handler.write_questions('sample_data/question.csv', new_question_data_items)
        return redirect('/list')
    return render_template('add_question.html')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id=None):
    all_questions = data_handler.read_questions('sample_data/question.csv')
    answer_fields = ['message', 'image']
    new_data_items = [0, question_id]
    line = {}
    for quest in all_questions:
        if quest['id'] == question_id:
            line = quest

    if request.method == 'POST':
        for field in answer_fields:
            if field == 'image':
                image_file = request.files.get('image')
                if image_file and allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    new_data_items.append(image_file.filename)
            else:
                new_data_items.append(request.form.get(field))
        data_handler.write_questions('sample_data/answer.csv', new_data_items)
        return redirect('/list')

    return render_template('post_answer.html', line=line)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id=None):
    all_answers = data_handler.read_questions('sample_data/answer.csv')
    new_all_answers = []
    for ans in all_answers:
        if ans['id'] == answer_id:
            continue
        else:
            new_all_answers.append(ans)
    data_handler.delete_line('sample_data/answer.csv', new_all_answers)
    return redirect('/list')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5000
    )
