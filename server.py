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
    latest_five = data_handler.display_five_latest_questions()
    return render_template('index.html', questions=latest_five)


@app.route('/contacts')
def contacts_page():
    return render_template('contacts.html')


@app.route('/about-us')
def about_us_page():
    return render_template('about-us.html')


@app.route('/list', methods=['GET', 'POST'])
def list_questions_page():
    questions = data_handler.read_table('question')
    headers = [table_header for table_header in questions[0]]
    for question in questions:
        question['submission_time'] = question['submission_time'].strftime("%Y.%m.%d")

    if request.method == 'POST':
        select_id = request.form.get('select_sort')
        questions = data_handler.read_table('question', select_id)

        return redirect(url_for('list_questions_page', questions=questions, headers=headers))
    return render_template('list.html', questions=questions, headers=headers)


@app.route('/question/<question_id>')
def question_details_page(question_id=None):
    question = data_handler.search_by_id('question', 'id', question_id)
    if question:
        question[0]['submission_time'] = question[0]['submission_time'].strftime("%Y.%m.%d %H:%M")
    answers = data_handler.search_by_id('answer', 'question_id', question_id)
    if answers:
        answers[0]['submission_time'] = answers[0]['submission_time'].strftime("%Y.%m.%d %H:%M")
    return render_template('question_details.html', question=question, answers=answers)


@app.route('/question/<question_id>/comments')
def question_comments_page(question_id=None):
    question = data_handler.search_by_id('question', 'id', question_id)
    comments = data_handler.search_by_id('comment', 'question_id', question_id)
    return render_template('question-comments.html', question=question, comments=comments)


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
    title = request.form.get('title')
    message = request.form.get('message')
    image = request.form.get('image')
    if request.method == 'POST':
        data_handler.add_question(title, message, image)
        return redirect(url_for('list_questions_page'))
    return render_template('add_question.html')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id=None):
    question = data_handler.search_by_id('question', 'id', question_id)

    if request.method == 'POST':
        updated_title = request.form.get('title')
        updated_message = request.form.get('message')
        data_handler.update_question(question_id, updated_title, updated_message)
        return redirect(url_for('question_details_page', question_id=question_id))

    return render_template('edit_question.html', question=question)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def post_answer(question_id):
    question = data_handler.search_by_id('question', 'id', question_id)

    if request.method == 'POST':
        message = request.form.get('message')
        image = request.form.get('image')
        data_handler.add_answer(question_id, message, image)
        return redirect(url_for('question_details_page', question_id=question_id))
    return render_template('post_answer.html', question=question)


@app.route('/answer/<answer_id>', methods=['GET', 'POST'])
def update_answer(answer_id):
    answer = data_handler.search_by_id('answer', 'id', answer_id)

    if request.method == 'POST':
        update_message = request.form.get('message')
        data_handler.update_answer(answer_id, update_message)
        return redirect('question_details_page')
    return render_template('edit-answer.html', answer=answer)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id=None):
    answer_data = data_handler.search_by_id('answer', 'id', answer_id)
    data_handler.delete_answer(answer_id)
    question_id = answer_data[0]['question_id']
    return redirect(url_for('question_details_page', question_id=question_id))


@app.route('/question/<question_id>/vote-down', methods=['GET', 'POST'])
def question_vote_down(question_id=None):
    data_handler.vote_down_question(question_id)
    return redirect(url_for('list_questions_page'))


@app.route('/question/<question_id>/vote-up', methods=['GET', 'POST'])
def question_vote_up(question_id=None):
    data_handler.vote_up_question(question_id)
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
    question = data_handler.get_question_by_answer_id(answer_id, )[0]
    question_id = question['question_id']
    data_handler.vote_up_answer(answer_id)
    return redirect(url_for('question_details_page', question_id=question_id))


@app.route('/answer/<answer_id>/vote-down', methods=['GET', 'POST'])
def answer_vote_down(answer_id=None):
    question = data_handler.get_question_by_answer_id(answer_id, )[0]
    question_id = question['question_id']
    data_handler.vote_down_answer(answer_id)
    return redirect(url_for('question_details_page', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        updated_message = request.form.get('message')
        data_handler.add_comment_to_question(question_id, updated_message)
        return redirect(url_for('question_details_page', question_id=question_id))
    return render_template('add-comment.html', question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    if request.method == 'POST':
        updated_message = request.form.get('message')
        data_handler.add_comment_to_answer(answer_id, updated_message)
        return redirect('/answer/<answer_id>')
    return render_template('new-comment.html', answer_id=answer_id)


@app.route('/answer/<answer_id>/delete_comment/<comment_id>', methods=['GET', 'POST'])
def delete_comment(comment_id):
    if request.method == 'GET':
        data_handler.delete_comment(comment_id)
        return redirect('/answer/<answer_id>')


@app.route('/answer/<answer_id>/comment/<comment_id>', methods=['GET', 'POST'])
def edit_answer_comment(comment_id, answer_id):
    comment = data_handler.get_comment_data(comment_id)
    if request.method == 'POST':
        edited_comment = request.form['message']
        edited_count = int(request.form['edited_count']) + 1
        data_handler.edit_comment(edited_comment, comment_id, edited_count)
        return redirect('answer/<answer_id>')
    return render_template('edit-comment.html', answer_id=answer_id, comment_id=comment_id, comment=comment)


@app.route('/question/<question_id>/comment/<comment_id>', methods=['GET', 'POST'])
def edit_question_comment(comment_id, question_id):
    comment = data_handler.get_comment_data(comment_id)
    if request.method == 'POST':
        edited_comment = request.form['message']
        edited_count = int(request.form['edited_count']) + 1
        data_handler.edit_comment(edited_comment, comment_id, edited_count)
        return redirect('question/<question_id>')
    return render_template('edit-comment.html', question_id=question_id, comment_id=comment_id, comment=comment)


@app.route('/question/<question_id>/tag', methods=['GET', 'POST'])
def add_tag(question_id):
    tags = data_handler.get_tag()
    if request.method == 'POST':
        new_tag = request.form.get('tag_name')
        data_handler.add_tag_to_table(new_tag)
        data_handler.add_tag_to_question(question_id, new_tag)
        return redirect('/question/<question_id>')
    return render_template('tag.html', question_id=question_id, tags=tags)


@app.route('/question/<question_id>/tag/<tag_id>/delete', methods=['GET', 'POST'])
def delete_tag(tag_id):
    if request.method == 'GET':
        data_handler.delete_tag(tag_id)
        return redirect('/question/<question_id>')


@app.route('/search')
def get_search_results():
    search_phrase = request.args.get('search-query')
    results = data_handler.find_search_results(search_phrase)
    headers = [header for header in results[0]]
    return render_template('search_results.html', results=results, headers=headers)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5200
    )

