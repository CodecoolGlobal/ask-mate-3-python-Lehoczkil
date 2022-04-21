from flask import Flask, render_template, redirect, url_for, request, session, flash
import data_handler
import os
import string
from werkzeug.utils import secure_filename

import database_common
from bonus_questions import SAMPLE_QUESTIONS

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)


@app.route('/')
def index_page():
    latest_questions = data_handler.display_latest_question()
    return render_template('index.html', questions=latest_questions)


@app.route("/bonus-questions")
def main():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


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
        button_value = request.form.get('select_sort').split(';')
        selected_order, selected_header = button_value
        questions = data_handler.read_table('question', selected_header, selected_order)
        for question in questions:
            question['submission_time'] = question['submission_time'].strftime("%Y.%m.%d")

    return render_template('list.html', questions=questions, headers=headers)


@app.route('/question/<question_id>')
def question_details_page(question_id=None):
    tags = data_handler.get_question_tags(question_id)
    question = data_handler.search_by_id('question', 'id', question_id)
    if question:
        question[0]['submission_time'] = question[0]['submission_time'].strftime("%Y.%m.%d %H:%M")
    answers = data_handler.search_by_id('answer', 'question_id', question_id)
    if answers:
        answers[0]['submission_time'] = answers[0]['submission_time'].strftime("%Y.%m.%d %H:%M")
    return render_template('question_details.html', question=question, answers=answers, tags=tags)


@app.route('/question/<question_id>/comments')
def question_comments_page(question_id=None):
    question = data_handler.search_by_id('question', 'id', question_id)
    comments = data_handler.search_by_id('comment', 'question_id', question_id)
    return render_template('question-comments.html', question=question, comments=comments)


@app.route('/answer/<answer_id>/comments')
def answer_comments_page(answer_id=None):
    answer = data_handler.search_by_id('answer', 'id', answer_id)
    comments = data_handler.search_by_id('comment', 'answer_id', answer_id)
    return render_template('answer-comments.html', answer=answer, comments=comments)


@app.route('/question/<question_id>/delete')
@database_common.login_required
def delete_question(question_id=None):
    data_handler.delete_record(table_name='question', record_id=question_id)
    return redirect(url_for('list_questions_page'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/add_question', methods=['GET', 'POST'])
@database_common.login_required
def add_question():
    question_fields = 'title', 'message', 'id', 'image'
    new_question_data_items = []
    if request.method == 'POST':
        for field in question_fields:
            if field == 'image':
                image_file = request.files.get('image')
                if image_file and allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    new_question_data_items.append(filename)
                new_question_data_items.append(None)
            elif field == 'id':
                session_user = session['username']
                user = data_handler.search_by_id('users', 'username', session_user)
                user_id = user[0]['id']
                new_question_data_items.append(user_id)
            else:
                new_question_data_items.append(request.form.get(field))
        data_handler.add_question(new_question_data_items)
        return redirect('/list')
    return render_template('add_question.html')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
@database_common.login_required
def edit_question(question_id=None):
    question = data_handler.search_by_id('question', 'id', question_id)

    if request.method == 'POST':
        updated_title = request.form.get('title')
        updated_message = request.form.get('message')
        data_handler.update_question(question_id, updated_title, updated_message)
        return redirect(url_for('question_details_page', question_id=question_id))

    return render_template('edit_question.html', question=question)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
@database_common.login_required
def post_answer(question_id=None):
    question = data_handler.search_by_id('question', 'id', question_id)
    answer_fields = 'message', 'id', 'image'
    new_answer_data_items = [question_id]
    if request.method == 'POST':
        for field in answer_fields:
            if field == 'image':
                image_file = request.files.get('image')
                if image_file and allowed_file(image_file.filename):
                    filename = secure_filename(image_file.filename)
                    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    new_answer_data_items.append(filename)
                new_answer_data_items.append(None)
            elif field == 'id':
                user = data_handler.search_by_id('users', 'username', session['username'])
                user_id = user[0]['id']
                new_answer_data_items.append(user_id)
            else:
                new_answer_data_items.append(request.form.get(field))
        data_handler.add_answer(new_answer_data_items)
        return redirect(url_for('question_details_page', question_id=question_id))
    return render_template('post_answer.html', question=question, question_id=question_id)


@app.route('/answer/<answer_id>', methods=['GET', 'POST'])
@database_common.login_required
def update_answer(answer_id):
    answer = data_handler.search_by_id('answer', 'id', answer_id)
    if request.method == 'POST':
        update_message = request.form.get('message')
        data_handler.update_answer(answer_id, update_message)
        return redirect(url_for('question_details_page', question_id=answer[0]['question_id']))
    return render_template('edit-answer.html', answer=answer)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
@database_common.login_required
def delete_answer(answer_id=None):
    answer_data = data_handler.search_by_id('answer', 'id', answer_id)
    data_handler.delete_record(table_name='answer', record_id=answer_id)
    question_id = answer_data[0]['question_id']
    return redirect(url_for('question_details_page', question_id=question_id))


@app.route('/question/<question_id>/vote-down', methods=['GET', 'POST'])
@database_common.login_required
def question_vote_down(question_id=None):
    data_handler.vote_down('question', question_id)
    return redirect(url_for('list_questions_page'))


@app.route('/question/<question_id>/vote-up', methods=['GET', 'POST'])
@database_common.login_required
def question_vote_up(question_id=None):
    data_handler.vote_up('question', question_id)
    return redirect(url_for('list_questions_page'))


@app.route('/answer/<answer_id>/vote-up', methods=['GET', 'POST'])
@database_common.login_required
def answer_vote_up(answer_id=None):
    question = data_handler.get_question_by_answer_id(answer_id)[0]
    question_id = question['question_id']
    data_handler.vote_up('answer', answer_id)
    return redirect(url_for('question_details_page', question_id=question_id))


@app.route('/answer/<answer_id>/vote-down', methods=['GET', 'POST'])
@database_common.login_required
def answer_vote_down(answer_id=None):
    question = data_handler.get_question_by_answer_id(answer_id)[0]
    question_id = question['question_id']
    data_handler.vote_down('answer', answer_id)
    return redirect(url_for('question_details_page', question_id=question_id))


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
@database_common.login_required
def add_comment_to_question(question_id):
    if request.method == 'POST':
        updated_message = request.form.get('message')
        user = data_handler.search_by_id('users', 'username', session['username'])
        user_id = user[0]['id']
        data_handler.add_comment_to_question(question_id, updated_message, user_id)
        return redirect(url_for('question_comments_page', question_id=question_id))
    return render_template('add-comment-to-question.html', question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
@database_common.login_required
def add_comment_to_answer(answer_id):
    if request.method == 'POST':
        updated_message = request.form.get('message')
        user = data_handler.search_by_id('users', 'username', session['username'])
        user_id = user[0]['id']
        data_handler.add_comment_to_answer(answer_id, updated_message, user_id)
        return redirect(url_for('answer_comments_page', answer_id=answer_id))
    return render_template('add-comment-to-answer.html', answer_id=answer_id)


@app.route('/question/<question_id>/delete_comment/<comment_id>', methods=['GET', 'POST'])
@database_common.login_required
def delete_question_comment(comment_id, question_id):
    data_handler.delete_comment(comment_id)
    return redirect(url_for('question_comments_page', question_id=question_id))


@app.route('/answer/<answer_id>/delete_comment/<comment_id>', methods=['GET', 'POST'])
@database_common.login_required
def delete_answer_comment(comment_id, answer_id):
    data_handler.delete_comment(comment_id)
    return redirect(url_for('answer_comments_page', answer_id=answer_id))


@app.route('/answer/<answer_id>/comment/<comment_id>', methods=['GET', 'POST'])
@database_common.login_required
def edit_answer_comment(comment_id, answer_id):
    comment = data_handler.search_by_id('comment', 'id', comment_id)
    if request.method == 'POST':
        new_message = request.form['message']
        data_handler.edit_comment(comment_id, new_message)
        return redirect(url_for('answer_comments_page', answer_id=answer_id))
    return render_template('edit-comment.html', answer_id=answer_id, comment=comment)


@app.route('/question/<question_id>/comment/<comment_id>', methods=['GET', 'POST'])
@database_common.login_required
def edit_question_comment(comment_id, question_id):
    comment = data_handler.search_by_id('comment', 'id', comment_id)
    if request.method == 'POST':
        new_message = request.form['message']
        data_handler.edit_comment(comment_id, new_message)
        return redirect(url_for('question_comments_page', question_id=comment[0]['question_id']))
    return render_template('edit-comment.html', question_id=question_id, comment=comment)


@app.route('/question/<question_id>/tag', methods=['GET', 'POST'])
@database_common.login_required
def add_tag(question_id=None):
    tags = data_handler.get_tag()
    question_tags = data_handler.get_question_tags(question_id)
    tag_names = [tag['name'] for tag in tags]
    if request.method == 'POST':
        new_tag = request.form.get('tag_name')
        if new_tag not in tag_names and new_tag not in ['', ' ', '  ', None]:
            tag_id = data_handler.add_tag_to_table(new_tag)
            data_handler.add_tag_to_question(question_id, tag_id)
            return redirect(url_for('question_details_page', question_id=question_id))
        existing_tag = request.form.get('tag')
        my_tag = data_handler.search_by_id('tag', 'name', existing_tag)
        data_handler.add_tag_to_question(question_id, int(my_tag[0]['id']))
        return redirect(url_for('question_details_page', question_id=question_id, tags=question_tags))
    return render_template('add-tag.html', question_id=question_id, tags=tags)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
@database_common.login_required
def delete_tag(question_id=None, tag_id=None):
    data_handler.delete_tag(tag_id)
    return redirect(url_for('question_details_page', question_id=question_id))


@app.route('/search')
def get_search_results():
    search_phrase = request.args.get('search-query')
    special_characters_to_exclude = string.punctuation
    table = str.maketrans('', '', special_characters_to_exclude)

    try:
        if search_phrase:
            search_phrase_words = search_phrase.split(' ')
            search_safe_words = [word.translate(table) for word in search_phrase_words]

            if '' not in search_safe_words:
                query_results = [data_handler.find_search_results(word) for word in search_safe_words]

                unique_results = []
                for result_item in query_results:
                    if result_item not in unique_results:
                        unique_results.append(result_item)

                headers = [header for header in query_results[0][0]]
            else:
                return redirect(request.referrer)
        else:
            return redirect(request.referrer)
    except IndexError:
        return render_template('search_results.html', message="No results found")

    return render_template('search_results.html', results=unique_results, headers=headers)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = data_handler.get_users()
        password = request.form.get('reg-password')
        password_again = request.form.get('reg-password-again')
        if password == '' or password_again == '':
            flash('Please enter a password')
            return redirect(url_for('register'))
        elif password == password_again:
            user_email = request.form.get('reg-email')
            if user_email == '':
                flash('Please enter your email address')
                return redirect(url_for('register'))
            first_name = request.form.get('first-name')
            last_name = request.form.get('last-name')
            if first_name != '' and last_name != '':
                if user_email in users[0]['username']:
                    flash('Email already in use')
                    return redirect(url_for('register'))
                else:
                    hashed_password = data_handler.hash_password(password)
                    print(hashed_password)
                    data_handler.add_user(user_email, first_name, last_name, hashed_password)
                    session['username'] = user_email
                    return redirect(url_for('index_page'))
            else:
                flash('Please enter a name', 'info')
                return redirect(url_for('register'))
        else:
            flash("Password doesn't match", 'info')
            return redirect(url_for('register'))
    elif "username" in session:
        flash('Already logged in')
        return redirect(url_for('index_page'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session:
        return redirect(url_for('index_page'))
    if request.method == 'POST':
        usernames = [data['username'] for data in data_handler.get_users()]
        username = request.form['username']
        input_password = request.form['password']
        if username in usernames:
            password = data_handler.get_password_by_username(username)['password']
            if data_handler.verify_password(input_password, password):
                session['username'] = username
                return redirect(url_for('index_page'))
            else:
                return render_template('login_form.html', error="password")
        else:
            return render_template('login_form.html', error="user")
    return render_template('login_form.html')


@app.route('/users')
def users():
    users_attributes = data_handler.list_users()
    headers = ['Username', 'Registration date', 'Questions', 'Answers', 'Comments', 'Reputation']
    logged_in = True if session else False
    return render_template('users.html', logged_in=logged_in, headers=headers, users_attributes_data_rows=users_attributes)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index_page'))
  

if __name__ == '__main__':
    app.run(
        host='localhost',
        debug=True,
        port=5200
    )
