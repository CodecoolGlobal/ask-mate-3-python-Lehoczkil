from flask import Flask, render_template, redirect, url_for, request
import data_handler


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/list')
def list_page():
    questions = data_handler.read_questions('sample_data/question.csv')
    headers = data_handler.DATA_HEADER
    return render_template('list.html', questions=questions, headers=headers)


@app.route('/question/<question_id>')
def questions_page():
    return render_template('questions.html')


@app.route('/add-question')
def add_question():
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
