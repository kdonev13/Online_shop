from functools import wraps

from flask import Flask
from flask import render_template, request, redirect, url_for, jsonify
import json

from user import User
from post import Post

app = Flask(__name__)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration_form.html')
    elif request.method == 'POST':
        values = (
            None,
            request.form['username'],
            User.hash_password(request.form['password']),
            request.form['email'],
            request.form['address'],
            request.form['telephone_number']
        )
        User(*values).add_user()

        return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login_form.html')
    elif request.method == 'POST':
        data = json.loads(request.data.decode('ascii'))
        email = data['email']
        password = data['password']
        user = User.find_by_email(email)
        if not user or not user.verify_password(password):
            return jsonify({'token': None})
        token = user.generate_token()
        return jsonify({'token': token.decode('ascii')})


if __name__ == '__main__':
    app.run(debug=True)