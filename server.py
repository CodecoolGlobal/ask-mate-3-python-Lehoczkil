from flask import Flask, render_template, redirect, url_for, request
import data_handler
import os
from werkzeug.utils import secure_filename

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
    headers = data_handler.DATA_HEADER
    return render_template('list.html', questions=questions, headers=headers)


@app.route('/question/<question_id>')
def questions_page(question_id=None):
    all_questions = data_handler.read_questions('sample_data/question.csv')
    question = {}
    for quest in all_questions:
        if quest['id'] == question_id:
            question = quest
            image = quest['image']
    all_answers = data_handler.read_questions('sample_data/answer.csv')
    answers = []
    for ans in all_answers:
        if ans['question_id'] == question_id:
            answers.append(ans)
    return render_template('questions.html', question=question, answers=answers, image=image)


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


@app.route('/question/<question_id>/new-answer')
def post_answer():
    return render_template('post_answer.html')


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5000
    )
